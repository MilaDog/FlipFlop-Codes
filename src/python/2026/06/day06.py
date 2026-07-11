from collections import defaultdict, deque
from dataclasses import dataclass
from enum import IntEnum
from typing import TypeVar


class LightLevel(IntEnum):
    """Available light levels."""

    OFF = 0
    LOW = 1
    HIGH = 2


@dataclass(frozen=True)
class Position:
    """Position of a tile."""

    x: int
    y: int


@dataclass
class Gear:
    """Representation of a gear tile."""

    position: Position
    gear_code: str
    is_shut_off: bool = False
    is_rotating_clockwise: bool = False


@dataclass
class Light:
    """Representation of a light tile."""

    position: Position
    gear_code: str
    light_level: LightLevel = LightLevel.OFF


@dataclass
class Bluetooth:
    """Representation of a Bluetooth tile."""

    position: Position
    id_: str
    is_input: bool = False
    is_rotating_clockwise: bool = False
    is_shut_off: bool = False
    has_been_activated: bool = False


@dataclass
class Background:
    """Representation of a clear tile."""

    position: Position


T = TypeVar("T", bound="Gear | Light | Bluetooth | Background")
Tile = Gear | Light | Bluetooth | Background


class Solution:
    """Solution for the problem."""

    def __init__(self, data: dict[Position, Tile], dimensions: tuple[int, int], starting_position: Position):
        self.data: dict[Position, Tile] = data
        self.start_position: Position = starting_position
        self.length: int = dimensions[0]
        self.width: int = dimensions[1]

        self.directions: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        data: dict[Position, Tile] = defaultdict()
        dimensions: tuple[int, int] = (-1, -1)
        starting_position: Position | None = None

        with open("./inputs/flipflopcodes/2026/input06.txt") as file:
            content = file.readlines()
            dimensions = (len(content), len(content[0]))

            for x, line in enumerate(content):
                for y, col in enumerate(line.strip()):
                    position: Position = Position(x=x, y=y)

                    match col:
                        case "S":
                            starting_position = position
                            data[position] = Gear(position=position, gear_code=col)

                        case "#" | "3":
                            data[position] = Gear(position=position, gear_code=col)

                        case "*":
                            data[position] = Light(position=position, gear_code="")

                        case _ if col.isupper():
                            data[position] = Bluetooth(position=position, id_=col)

                        case _ if col.islower():
                            data[position] = Bluetooth(position=position, is_input=True, id_=col)

                        case _:
                            data[position] = Background(position=position)

        if starting_position is None:
            raise Exception("Starting position cannot be found.")

        return cls(data=data, dimensions=dimensions, starting_position=starting_position)

    def display(self) -> None:
        """Display the grid."""
        keys: str = """
        KEYS:
        ================================
        L -> rotating counter-clockwise
        R -> rotating clockwise
        . -> Background
        aA -> Bluetooth sender-receiver
        o|%|# -> Light OFF | LOW | HIGH
        """
        print(keys, end="\n\n")

        for x in range(self.length):
            for y in range(self.width):
                target_tile: Tile | None = self.data.get(Position(x=x, y=y), None)

                if target_tile is not None:
                    match target_tile:
                        case Gear():
                            if target_tile.is_shut_off:
                                print("X", end="")

                            else:
                                print(
                                    "R" if target_tile.is_rotating_clockwise else "L",
                                    end="",
                                )

                        case Light(light_level=l):
                            match l:
                                case LightLevel.OFF:
                                    print("o", end="")

                                case LightLevel.LOW:
                                    print("%", end="")

                                case LightLevel.HIGH:
                                    print("#", end="")

                        case Background():
                            print(".", end="")

                        case Bluetooth():
                            print(target_tile.id_, end="")

            print()
        print()

    def is_prime(self, num: int) -> bool:
        """Determine if the given number is prime or not.

        Args:
            num (int): Number to check.

        Returns:
            bool: If the number is prime or not.
        """
        if num < 2:
            return False
        return all(num % i for i in range(2, int(num**0.5) + 1))

    def is_within_grid(self, position: Position) -> bool:
        """Determine whether the given position falls within the grid.

        Args:
            position (Position): Position of the tile.

        Returns:
            bool: Whether position is within the grid or not.
        """
        return 0 <= position.x < self.length and 0 <= position.y < self.width

    def get_adjacent_tiles(self, tile: Tile) -> list[Tile]:
        """Get the adjacent gears to a given position.

        Args:
            tile (Tile): Tile in the grid.

        Returns:
            list[tuple[int, int]]: All positions of adjacent gears.
        """
        res: list[Tile] = []

        for dx, dy in self.directions:
            target_position: Position = Position(tile.position.x + dx, tile.position.y + dy)

            if not self.is_within_grid(position=target_position):
                continue

            target_tile: Tile | None = self.data.get(target_position, None)
            if target_tile is not None:
                res.append(target_tile)

        return res

    def get_adjacent_of_type(self, tile: Tile, cls: type[T]) -> list[T]:
        """Get all adjacent gears to the given tile.

        Args:
            tile (Tile): Tile to search around.
            cls: Type of tile to filter by.

        Returns:
            list[Tile]: All tiles of the given type.
        """
        return [t for t in self.get_adjacent_tiles(tile=tile) if isinstance(t, cls)]

    def _perform_bfs(self, position: Position, func) -> None:
        q: deque = deque([self.data.get(position)])
        seen: set[Position] = set()

        while q:
            tile = q.popleft()

            if tile is None or tile.position in seen:
                continue
            seen.add(tile.position)

            if not isinstance(tile, (Gear, Bluetooth)):
                continue

            func(tile)
            q.extend(self.get_adjacent_of_type(tile=tile, cls=Gear))

    def get_connected_bluetooth_tiles(self, position: Position) -> list[Bluetooth]:
        """Get a list of all positions of bluetooth devices connected to the section of gears.

        Args:
            position (Position): Starting position of gear section.

        Returns:
            list[Tile]: List of all bluetooth tile positions found.
        """
        res: list[Bluetooth] = []

        def visit(tile: Gear | Bluetooth) -> None:
            for bt_device in self.get_adjacent_of_type(tile=tile, cls=Bluetooth):
                bt_device.is_rotating_clockwise = tile.is_rotating_clockwise
                res.append(bt_device)

        self._perform_bfs(position=position, func=visit)
        return res

    def get_connected_gears(self, position: Position) -> list[Gear]:
        """Get a list of all connected gears to the given position.

        Args:
            position (Position): Position to search around.

        Returns:
            list[Tile]: List of all found connected Gears.
        """
        res: list[Gear] = []
        self._perform_bfs(position=position, func=lambda tile: res.append(tile) if isinstance(tile, Gear) else None)
        return res

    def rotate_gears(self, position: Position, is_rotating_clockwise: bool) -> None:
        """Rotate the gears in the grid starting that the given position with the given rotation direction.

        Args:
            position (Position): Starting position.
            is_rotating_clockwise (bool): If the initial rotation is clockwise.
        """
        q: deque = deque()
        q.append((self.data.get(position), is_rotating_clockwise))
        seen: set[Position] = set()

        while q:
            tile, is_rotating_clockwise = q.popleft()

            if tile is None or tile.position in seen:
                continue

            seen.add(tile.position)
            match tile:
                case Gear():
                    if tile.is_shut_off:
                        continue

                    tile.is_rotating_clockwise = is_rotating_clockwise

                case Bluetooth():
                    pass

                case _:
                    continue

            for neighbour in self.get_adjacent_of_type(tile=tile, cls=Gear):
                q.append((neighbour, not is_rotating_clockwise))

    def update_light_levels(self) -> None:
        """Determine the light level of each light tile in the grid."""
        for x in range(self.length):
            for y in range(self.width):
                target_tile: Tile | None = self.data.get(Position(x=x, y=y), None)

                if isinstance(target_tile, Light):
                    adjacent_gears: list[Gear] = self.get_adjacent_of_type(tile=target_tile, cls=Gear)

                    if not adjacent_gears:
                        continue

                    target_gear = adjacent_gears[0]
                    target_tile.light_level = (
                        LightLevel.OFF
                        if target_gear.is_shut_off
                        else LightLevel.HIGH
                        if target_gear.is_rotating_clockwise
                        else LightLevel.LOW
                    )
                    target_tile.gear_code = target_gear.gear_code

    def determine_lights_code(self, gear_codes: str) -> int:
        """Determine the code from the given lights in the grid.

        Args:
            gear_codes (str): Codes of gears to consider.

        Returns:
            int: Determined code. -1 if nothing found.
        """
        code: str = ""

        for x in range(self.length):
            for y in range(self.width):
                match target_tile := self.data.get(Position(x=x, y=y), None):
                    case Light(light_level=l):
                        if target_tile.gear_code not in gear_codes:
                            continue

                        match l:
                            case LightLevel.HIGH:
                                code += "1"
                            case LightLevel.LOW:
                                code += "0"
                            case _:
                                pass

        if len(code) == 0:
            return -1

        return int(code, 2)

    def activate_bluetooth_signals(self, perform_prime_ruling: bool = False) -> None:
        """Activate bluetooth signals, leading to the rotation of the new gears.

        Args:
            perform_prime_ruling (bool): Whether to allow for the rotating of gears to bluetooth signals or not.
        """
        # start at the `starting_position`.
        # Find all bluetooth devices connected.
        # Activate each bluetooth device.
        # Turn corresponding gears.
        # Repeat process.

        bluetooth_tiles: defaultdict[str, Bluetooth] = defaultdict()
        for tile in self.data.values():
            if isinstance(tile, Bluetooth) and tile.id_.isupper():
                bluetooth_tiles[tile.id_.lower()] = tile

        q: deque = deque()

        for bt_device in self.get_connected_bluetooth_tiles(position=self.start_position):
            q.append(bt_device)

        while q:
            device = q.popleft()

            if isinstance(device, Bluetooth) and device.has_been_activated:
                continue

            device.has_been_activated = True
            receiver: Bluetooth | None = bluetooth_tiles.get(device.id_.lower())

            if receiver is not None:
                receiver.has_been_activated = True
                receiver.is_shut_off = device.is_shut_off

                if not perform_prime_ruling:
                    self.rotate_gears(position=receiver.position, is_rotating_clockwise=device.is_rotating_clockwise)

                else:  # Part 03
                    if not receiver.is_shut_off:
                        connected_gears_to_bt_device: list[Gear] = self.get_connected_gears(position=receiver.position)
                        not_performing_gear_rotating: bool = self.is_prime(num=len(connected_gears_to_bt_device))

                        if not_performing_gear_rotating:
                            receiver.is_shut_off = True

                        else:
                            self.rotate_gears(
                                position=receiver.position, is_rotating_clockwise=device.is_rotating_clockwise
                            )

                # lock gears
                if receiver.is_shut_off:
                    for gear in self.get_connected_gears(position=receiver.position):
                        if isinstance(gear, Gear):
                            gear.is_shut_off = True

                for bt_device in self.get_connected_bluetooth_tiles(position=receiver.position):
                    if isinstance(bt_device, Bluetooth):
                        bt_device.is_shut_off = receiver.is_shut_off
                        q.append(bt_device)

    def solve(self) -> None:
        """Solution."""
        # Part 01
        self.rotate_gears(position=self.start_position, is_rotating_clockwise=False)
        self.update_light_levels()
        tlt: int = self.determine_lights_code(gear_codes="#")
        print(f"Part 01: {tlt}")

        # Part 02
        self.activate_bluetooth_signals()
        self.update_light_levels()
        tlt = self.determine_lights_code(gear_codes="#3")
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        self.rotate_gears(position=self.start_position, is_rotating_clockwise=False)
        self.activate_bluetooth_signals(perform_prime_ruling=True)
        self.update_light_levels()
        tlt = self.determine_lights_code(gear_codes="#3")
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol_p1_p2: Solution = Solution.parse()
    sol_p1_p2.solve()

    sol_p3: Solution = Solution.parse()
    sol_p3.part03()
