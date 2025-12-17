import math
from functools import reduce
from operator import mul

type Grid = tuple[int, ...]


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[Grid]):
        self.data: list[Grid] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        values: list[Grid] = []

        with open("./inputs/flipflopcodes/2025/07/input.txt") as file:
            for line in file.readlines():
                values.append(tuple(map(int, line.strip().split(" "))))

        return cls(data=values)

    def calculate_number_paths_in_grid(self, dimensions: list[int]) -> int:
        """Calculate the number of paths from the two farthest points in the grid.

        Args:
            dimensions (list[int]): Dimensions of the grid.

        Returns:
            int: Number of paths.
        """
        moves: list[int] = [d - 1 for d in dimensions]
        total: int = sum(moves)

        # total! / (m1! * m2! * m3! *...)
        numerator: int = math.factorial(total)
        denominator: int = reduce(mul, (math.factorial(m) for m in moves), 1)

        return numerator // denominator

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = sum(self.calculate_number_paths_in_grid(dimensions=list(grid)) for grid in self.data)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        for grid in self.data:
            dimensions: list[int] = list(grid)
            dimensions.append(grid[0])
            tlt += self.calculate_number_paths_in_grid(dimensions=dimensions)

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = 0

        for grid in self.data:
            type_, size, *_ = grid
            dimensions: list[int] = [size] * type_
            tlt += self.calculate_number_paths_in_grid(dimensions=dimensions)

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
