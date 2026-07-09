from copy import deepcopy


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2026/04/input.txt") as file:
            values: list[str] = [line.replace("\n", "") for line in file.readlines()][
                ::-1
            ]  # having the ground at index 0

        return cls(data=values)

    def part01(self) -> None:
        """Solution to Part 01."""
        cut: int = 400
        tlt: int = sum(line.count("o") for line in self.data[cut + 1 :])
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0

        prev_index: int = -1
        for leaf in self.data:
            try:
                pos: int = leaf.index("o")

                if prev_index == -1:
                    prev_index = pos
                    continue

                if pos != prev_index:
                    tlt += 1
                    prev_index = pos

            except ValueError:
                continue

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = 0

        flower: list[str] = deepcopy(self.data)
        while True:
            made_move: bool = False
            set_initial_position: bool = False
            prev_flower_side: int = -1
            prev_flower_index: int = -1

            for i, leaf in enumerate(deepcopy(flower)):
                try:
                    pos: int = leaf.index("o")

                    if pos != prev_flower_side or not set_initial_position:
                        set_initial_position = True
                        prev_flower_side = pos
                        prev_flower_index = i
                        flower[i] = "  |  "  # remove leaf
                        made_move = True

                except ValueError:
                    if "/" in leaf:
                        flower[prev_flower_index] = "  |  "  # remove leaf due to jumping to flower

                    continue

            if not made_move:
                break

            tlt += 1

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
