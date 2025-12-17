from collections import deque

type Coords = tuple[int, ...]


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[Coords]):
        self.data: list[Coords] = data
        self.beach_size: tuple[int, int] = (101, 101)

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        values: list[Coords] = []

        with open("./inputs/flipflopcodes/2025/04/input.txt") as file:
            for line in file.readlines():
                values.append(tuple(map(int, line.strip().split(","))))

        return cls(data=values)

    def _is_within_bounds(self, coords: Coords) -> bool:
        """Determine whether `coords` is within the bounds of the grid.

        Args:
            coords (Coords): Position to check.

        Returns:
            bool: Whether the position is within the grid bounds.
        """
        return 0 <= coords[0] < self.beach_size[0] and 0 <= coords[1] < self.beach_size[1]

    def _traverse(self, start: Coords, end: Coords, include_diagonals: bool = False) -> int:
        """Traverse the grid for the shortest path from `start` to `end`.

        Args:
            start (Coords): Starting position.
            end (Coords): Ending position.
            include_diagonals (bool): Whether to include diagonal movements. FALSE by default.

        Returns:
            int: Number of steps taken from `start` to `end`.
        """
        movements: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        if include_diagonals:
            movements += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        seen: set[Coords] = set()
        q: deque[tuple[int, Coords]] = deque([(0, start)])

        while q:
            curr_steps, curr, *_ = q.popleft()

            if curr in seen:
                continue

            if curr == end:
                return curr_steps

            seen.add(curr)
            x, y = curr

            for dx, dy in movements:
                new_pos: tuple[int, int] = (dx + x, dy + y)

                if self._is_within_bounds(coords=new_pos):
                    q.append((curr_steps + 1, new_pos))

        return -1

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = 0

        start: tuple[int, ...] = (0, 0)
        for coord in self.data:
            tlt += self._traverse(start=start, end=coord)
            start = coord

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        start: tuple[int, ...] = (0, 0)
        for coord in self.data:
            tlt += self._traverse(start=start, end=coord, include_diagonals=True)
            start = coord

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = 0

        start: tuple[int, ...] = (0, 0)
        for coord in sorted(self.data[:], key=lambda x: sum(x)):
            tlt += self._traverse(start=start, end=coord, include_diagonals=True)
            start = coord

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
