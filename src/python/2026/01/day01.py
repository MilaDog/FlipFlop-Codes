class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[int]):
        self.data: list[int] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2026/01/input.txt") as file:
            values: list[int] = [int(line.strip()) for line in file.readlines()]

        return cls(data=values)

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = sum(max(60 - line, 0) for line in self.data)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        for line in self.data:
            diff: int = 60 - line
            tlt += diff if diff > 0 else abs(diff) * 5

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        lngth: int = len(self.data) // 2

        coffee_temps: list[int] = self.data[:lngth]
        preferred_temps: list[int] = self.data[lngth:]

        tlt: int = 0

        for t1, t2 in zip(coffee_temps, preferred_temps):
            diff: int = t2 - t1
            tlt += diff if diff > 0 else abs(diff) * 5

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
