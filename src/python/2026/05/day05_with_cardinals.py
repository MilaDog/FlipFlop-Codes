from copy import deepcopy
from dataclasses import dataclass, field
from queue import Queue


@dataclass
class Entry:
    """Representation of a movement entry for traversing the grid, replacing the symbols `^>v<` with their
    corresponding cardinal direction.

    Was bored and wondered if you could eliminate the original `dict` lookups for performing right turns and
    updating positions.
    """

    position: tuple[int, int]
    score: int = 0
    has_made_change: bool = False
    right_turns_made: int = 0
    seen: set[tuple[int, int]] = field(default_factory=set)

    def has_visited(self) -> bool:
        """If the current position has been visited yet.

        Returns:
            bool: If the current position has been visited.
        """
        return self.position in self.seen

    def visit(self) -> None:
        """Visit position."""
        self.seen.add(self.position)

    def update_position(self, cardinal_direction: int) -> None:
        """Update the position of the entry according to the set directions list.

        Args:
            cardinal_direction (int): Direction symbol to move in.
        """
        x, y = self.position

        match cardinal_direction:
            case 0:
                self.position = (x - 1, y)
            case 90:
                self.position = (x, y + 1)
            case 180:
                self.position = (x + 1, y)
            case 270:
                self.position = (x, y - 1)
            case _:
                raise Exception(f"Unknown direction symbol given: {cardinal_direction}")

    def perform_right_turn(self, cardinal_direction: int) -> None:
        """Perform a right turn on the position.

        Args:
            cardinal_direction (int): New symbol direction to follow.
        """
        self.right_turns_made += 1
        self.update_position(cardinal_direction=(cardinal_direction + 90) % 360)


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[list[int]]):
        self.data: list[list[int]] = data
        self.length: int = len(self.data)
        self.width: int = len(self.data[0])

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2026/05/input.txt") as file:
            dirrs = {"<": 270, ">": 90, "^": 0, "v": 180}  # cardinal directions
            values: list[list[int]] = [[dirrs[x] for x in line.strip()] for line in file.readlines()]

        return cls(data=values)

    def is_on_grid_edge(self, entry: Entry) -> bool:
        """Determine if the given position falls on the edge of the grid.

        Args:
            entry (Entry): Entry object.

        Returns:
            bool: Whether on the edge of the grid or not.
        """
        return entry.position[0] in (0, self.length - 1) or entry.position[1] in (0, self.width - 1)

    def traverse_grid(
        self, start_position: tuple[int, int], allow_direction_change: bool = False, allow_right_turns: bool = False
    ) -> int:
        """Traverse the grid from the given position, returning the longest taken unique path.

        Args:
            start_position (tuple[int, int]): Starting position in the grid.
            allow_direction_change (bool): Whether to allow for direction changes. Default is FALSE.
            allow_right_turns (bool): Whether to allow for right turns. Default is FALSE.

        Returns:
            int: Longest unique traversed path.
        """
        max_score: int = 0

        q: Queue[Entry] = Queue()
        q.put(Entry(position=start_position))

        while not q.empty():
            entry: Entry = q.get()
            symbol: int = self.data[entry.position[0]][entry.position[1]]

            if entry.has_visited():
                if entry.score > max_score:
                    max_score = entry.score

                # P03 logic
                if allow_right_turns:
                    if self.is_on_grid_edge(entry=entry):
                        continue

                    # making a right turn
                    if entry.right_turns_made < 3:
                        new_entry: Entry = deepcopy(entry)
                        new_entry.perform_right_turn(cardinal_direction=symbol)
                        q.put(new_entry)

                continue

            entry.visit()
            entry.score += 1

            if allow_direction_change:
                if self.is_on_grid_edge(entry=entry):
                    entry.update_position(cardinal_direction=symbol)
                    q.put(entry)
                    continue

                # add all possible other directions for the current position
                if not entry.has_made_change:
                    for dirr in range(0, 360, 90):
                        new_entry: Entry = deepcopy(entry)
                        new_entry.update_position(cardinal_direction=dirr)
                        new_entry.has_made_change = dirr != symbol
                        q.put(new_entry)
                    continue

                entry.update_position(cardinal_direction=symbol)
                q.put(entry)

            else:
                entry.update_position(cardinal_direction=symbol)
                entry.has_made_change = True
                q.put(entry)

        return max_score

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = self.traverse_grid(start_position=(0, 0))
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = self.traverse_grid(start_position=(0, 0), allow_direction_change=True)
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = self.traverse_grid(start_position=(0, 0), allow_direction_change=True, allow_right_turns=True)
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
