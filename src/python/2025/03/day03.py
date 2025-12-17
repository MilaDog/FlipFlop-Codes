from collections import Counter

type RGB = tuple[int, ...]


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[RGB]):
        self.data: list[RGB] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        values: list[RGB] = []

        with open("./inputs/flipflopcodes/2025/03/input.txt") as file:
            for line in file.readlines():
                values.append(tuple(map(int, line.strip().split(","))))

        return cls(data=values)

    def part01(self) -> None:
        """Solution to Part 01."""
        cnter: Counter = Counter(self.data)
        res: str = ",".join(map(str, cnter.most_common(n=1)[0][0]))

        print(f"Part 01: {res}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        for r, g, b in self.data:
            # Special
            if any([r == b, r == g, g == b, r == g == b]):
                continue

            tlt += g > b and g > r

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = 0

        for r, g, b in self.data:
            # Special
            if any([r == b, r == g, g == b, r == g == b]):
                tlt += 10
                continue

            # Red
            if r > b and r > g:
                tlt += 5
                continue

            # Green
            if g > b and g > r:
                tlt += 2
                continue

            # Blue
            if b > g and b > r:
                tlt += 4
                continue

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
