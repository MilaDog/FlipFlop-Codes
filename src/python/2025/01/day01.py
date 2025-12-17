class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2025/01/input.txt") as file:
            values: list[str] = [line.strip() for line in file.readlines()]

        return cls(data=values)

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = sum(len(line) // 2 for line in self.data)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        for line in self.data:
            if (x := len(line) // 2) % 2 == 0:
                tlt += x

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = sum(len(line) // 2 for line in filter(lambda val: "e" not in val, self.data))
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
