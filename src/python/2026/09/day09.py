from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import cache


@dataclass(frozen=True)
class Position:
    """Position within the grid."""

    x: int
    y: int

    def is_none(self) -> bool:
        """Position is not valid."""
        return self.x == -1 and self.y == -1

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Position):
            return False

        if value.is_none() or self.is_none():
            return False

        return value.x == self.x and value.y == self.y

    def __lt__(self, other) -> bool:
        if not isinstance(other, Position):
            return False

        if other.is_none() or self.is_none():
            return False

        return self.x < other.x and self.y < other.y


@dataclass(frozen=True)
class Teleport:
    """Representation of a teleport move."""

    position: Position
    performed_teleport: bool = False


class Direction(Enum):
    """All potential moving direction."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def values() -> list["Direction"]:
        """Get a list of all directions."""
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


State = tuple[Position, Position, Position]


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[list[str]], start: Position, end: Position):
        self.data: list[list[str]] = data
        self.start: Position = start
        self.end: Position = end

        self.length: int = len(self.data)
        self.width: int = len(self.data[0])

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        data: list[list[str]] = []
        start: Position | None = None
        end: Position | None = None

        with open("./inputs/flipflopcodes/2026/input09.txt") as file:
            for x, line in enumerate(file.readlines()):
                r: list[str] = []

                for y, tile in enumerate(line.strip()):
                    if tile == "S":
                        start = Position(x=x, y=y)
                        tile = "."

                    if tile == "E":
                        end = Position(x=x, y=y)
                        tile = "."

                    r.append(tile)

                data.append(r)

        if start is None or end is None:
            raise Exception("Cannot find starting/ending position in the maze...")

        return cls(data=data, start=start, end=end)

    def display(self, player_location: Position) -> None:
        """Display the maze."""
        for x in range(self.length):
            for y in range(self.width):
                sym: str = self.data[x][y]

                if Position(x, y) == self.start:
                    sym = "S"

                if Position(x, y) == self.end:
                    sym = "E"

                if Position(x, y) == player_location:
                    sym = "Y"

                print(sym, end="")
            print()

    def _within_grid(self, position: Position) -> bool:
        """Check whether the given position is within the maze bounds.

        Args:
            position (Position): Position to check within the grid.

        Returns:
            bool: Within maze or not.
        """
        return 0 <= position.x < self.length and 0 <= position.y < self.width

    @cache
    def _teleport(self, position: Position, direction: Direction, max_length: int = -1) -> tuple[bool, Position]:
        """Teleport to a new position from the given position in the target direction, returning a teleport move.

        Args:
            position (Position): Position to teleport from.
            direction (Direction): Direction to travel in.
            max_length (int): Max length of a teleport. Use -1 to move as far as possible.

        Returns:
            tuple[boo, Position]: Whether the teleport occurred and the resulting position.
        """
        # checking that the initial position is not an invalid spot
        if self.data[position.x][position.y] == "#":
            return False, position

        tiles_covered: set[Position] = set()

        while True:
            if 0 >= max_length == len(tiles_covered):
                break

            dx, dy = direction.value
            new_position: Position = Position(x=position.x + dx, y=position.y + dy)

            # hit wall or outside of grid, cannot go any further
            if not self._within_grid(position=new_position) or self.data[new_position.x][new_position.y] == "#":
                break

            # move onto tile
            tiles_covered.add(position)
            position = new_position

        return True, position

    def _canonical_state(self, current: Position, portal_01: Position, portal_02: Position) -> State:
        if portal_01.is_none() or portal_02.is_none():
            return current, portal_01, portal_02

        if portal_02 < portal_01:
            portal_01, portal_02 = portal_02, portal_01

        return current, portal_01, portal_02

    def traverse(self, with_teleports: bool = False, with_portal_use: bool = False) -> int:
        """Traverse the maze, returning the shortest path taken.

        Args:
            with_teleports (bool): Whether to allow for teleportation within the maze.
            with_portal_use (bool): Whether to allow for the use of portals within the maze.

        Returns:
            int: Shortest path taken.
        """
        initial_state: tuple[Position, Position, Position] = (self.start, Position(x=-1, y=-1), Position(x=-1, y=-1))
        q: deque = deque([(initial_state, 0)])
        visited: set[tuple[Position, Position, Position]] = {initial_state}

        while q:
            curr_state, score = q.popleft()
            curr_pos, portal_01, portal_02 = curr_state

            if curr_pos == self.end:
                return score

            if with_teleports:  # Part 02
                for direction in Direction.values():
                    did_teleport, resulting_position = self._teleport(position=curr_pos, direction=direction)

                    if did_teleport and resulting_position != curr_pos:
                        new_state = self._canonical_state(resulting_position, portal_01, portal_02)

                        if new_state not in visited:
                            visited.add(new_state)
                            q.append((new_state, score + 1))

            if with_portal_use:  # Part 03
                for direction in Direction.values():
                    did_fire, resulting_portal_position = self._teleport(position=curr_pos, direction=direction)

                    if did_fire and resulting_portal_position != curr_pos:
                        for shot_state in (
                            (curr_pos, resulting_portal_position, portal_02),
                            (curr_pos, portal_01, resulting_portal_position),
                        ):
                            shot_state = self._canonical_state(*shot_state)

                            if curr_state == shot_state:
                                continue

                            if shot_state not in visited:
                                visited.add(shot_state)
                                q.append((shot_state, score + 1))

            # moving a single tile
            for direction in Direction.values():
                dx, dy = direction.value
                new_position: Position = Position(x=curr_pos.x + dx, y=curr_pos.y + dy)

                if not self._within_grid(position=new_position) or self.data[new_position.x][new_position.y] != ".":
                    continue

                # stepping into portal
                if with_portal_use and not portal_01.is_none() and not portal_02.is_none():
                    if new_position == portal_01:
                        new_position = portal_02

                    elif new_position == portal_02:
                        new_position = portal_01

                new_state = self._canonical_state(new_position, portal_01, portal_02)
                if new_state not in visited:
                    visited.add(new_state)
                    q.append((new_state, score + 1))

        return -1

    def part01(self) -> None:
        """Solution to Part 01."""
        print(f"Part 01: {self.traverse()}")

    def part02(self) -> None:
        """Solution to Part 02."""
        print(f"Part 02: {self.traverse(with_teleports=True)}")

    def part03(self) -> None:
        """Solution to Part 03."""
        print(f"Part 03: {self.traverse(with_portal_use=True)}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
