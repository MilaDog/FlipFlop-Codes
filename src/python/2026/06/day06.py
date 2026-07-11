from collections import defaultdict, deque
from dataclasses import dataclass
from enum import IntEnum


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


@dataclass
class Background:
    """Representation of a clear tile."""

    position: Position


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
        KEYS:\n================================\n
        L -> rotating counter-clockwise\n
        R -> rotating clockwise\n
        . -> Background\naA -> Bluetooth sender-receiver\n
        o|%|# -> Light OFF | LOW | HIGH"""
        print(keys, end="\n\n")

        for x in range(self.length):
            for y in range(self.width):
                target_tile: Tile | None = self.data.get(Position(x=x, y=y), None)

                if target_tile is not None:
                    match target_tile:
                        case Gear():
                            print("R" if target_tile.is_rotating_clockwise else "L", end="")

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

    def is_within_grid(self, x: int, y: int) -> bool:
        """Determine whether the given position falls within the grid.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: Whether position is within the grid or not.
        """
        return 0 <= x < self.length and 0 <= y < self.width

    def get_adjacent_gears(self, tile: Tile) -> list[Position]:
        """Get the adjacent gears to a given position.

        Args:
            tile (Tile): Tile in the grid.

        Returns:
            list[tuple[int, int]]: All positions of adjacent gears.
        """
        res: list[Position] = []

        for dx, dy in self.directions:
            if not self.is_within_grid(x=tile.position.x + dx, y=tile.position.y + dy):
                continue

            match self.data.get(Position(tile.position.x + dx, tile.position.y + dy), None):
                case Gear():
                    res.append(Position(tile.position.x + dx, tile.position.y + dy))

                case _:
                    continue

        return res

    def rotate_gears(self, position: Position, is_rotating_clockwise: bool) -> None:
        """Rotate the gears in the grid starting that the given position with the given rotation direction.

        Args:
            position (Position): Starting position.
            is_rotating_clockwise (bool): If the initial rotation is clockwise.
        """
        q: deque = deque()
        q.append((position, is_rotating_clockwise))
        seen: set[Position] = set()

        while q:
            pos, is_rotating_clockwise = q.popleft()

            if pos in seen:
                continue

            seen.add(pos)
            target_tile: Tile | None = self.data.get(pos, None)

            if target_tile is not None:
                match target_tile:
                    case Gear():
                        target_tile.is_rotating_clockwise = is_rotating_clockwise

                    case Bluetooth():
                        pass

                    case _:
                        continue

                for neighbour in self.get_adjacent_gears(tile=target_tile):
                    q.append((neighbour, not is_rotating_clockwise))

    def update_light_levels(self) -> None:
        """Determine the light level of each light tile in the grid."""
        for x in range(self.length):
            for y in range(self.width):
                target_tile: Tile | None = self.data.get(Position(x=x, y=y), None)

                match target_tile:
                    case Light():
                        adjacent_gear: list[Position] = self.get_adjacent_gears(tile=target_tile)

                        if not adjacent_gear:
                            continue

                        target_gear: Tile | None = self.data.get(adjacent_gear[0], None)

                        if target_gear is not None:
                            match target_gear:
                                case Gear(is_rotating_clockwise=r):
                                    target_tile.light_level = LightLevel.HIGH if r else LightLevel.LOW
                                    target_tile.gear_code = target_gear.gear_code

                    case _:
                        pass

    def determine_lights_code(self, gear_codes: str) -> int:
        """Determine the code from the given lights in the grid.

        Args:
            gear_codes (str): Codes of gears to consider.

        Returns:
            int: Determined code. -1 if nothing found.
        """
        code: str = ""

        light_tiles: list[Tile] = list(filter(lambda x: isinstance(x, Light), self.data.values()))

        for light_tile in sorted(light_tiles, key=lambda tile: (tile.position.x, tile.position.y)):
            match light_tile:
                case Light(light_level=l):
                    if light_tile.gear_code not in gear_codes:
                        continue

                    match l:
                        case LightLevel.HIGH:
                            code += "1"
                        case LightLevel.LOW:
                            code += "0"
                        case _:
                            pass

                case _:
                    continue

        if len(code) == 0:
            return -1

        return int(code, 2)

    def activate_bluetooth_signals(self) -> None:
        """Activate bluetooth signals, leading to the rotation of the new gears."""
        bluetooth_tiles: defaultdict[str, list[Bluetooth]] = defaultdict(list)

        for tile in self.data.values():
            if isinstance(tile, Bluetooth):
                bluetooth_tiles[tile.id_.lower()].append(tile)

        for bluetooth_devices in bluetooth_tiles.values():
            sender, receiver, *_ = sorted(bluetooth_devices, key=lambda x: not x.is_input)
            adjacent_gears: list[Position] = self.get_adjacent_gears(tile=sender)

            if len(adjacent_gears) != 0:
                target_gear: Tile | None = self.data.get(adjacent_gears[0], None)

                if target_gear is not None and isinstance(target_gear, Gear):
                    sender.is_rotating_clockwise = target_gear.is_rotating_clockwise
                    receiver.is_rotating_clockwise = target_gear.is_rotating_clockwise

                    # update nearby gears
                    self.rotate_gears(position=receiver.position, is_rotating_clockwise=receiver.is_rotating_clockwise)

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
        tlt: int = 0
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.solve()
