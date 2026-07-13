from collections import Counter, defaultdict
from itertools import pairwise


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        data: list[str] = []

        with open("./inputs/flipflopcodes/2026/input08.txt") as file:
            data = [line.strip() for line in file.readlines()]

        return cls(data=data)

    def evolve(self, stoat: str, generations: int, in_pairs: bool = False) -> int:
        """Evolve the given stoat according to the evolution rules for the given number of generations, returning
        the final score after all generations have been completed.

        Args:
            stoat (str): Starting stoat.
            generations (int): Number of generations to perform.
            in_pairs (bool): Whether to evolve in pairs.

        Returns:
            int: Digital score of the stoat after all generations.
        """
        all_stoats: dict[str, list[str]] = defaultdict(list)

        for entry in self.data:
            entry = entry.replace(" ", "")
            group: str = entry[: 1 + in_pairs]

            all_stoats[group].append(entry[1 + in_pairs :])

            if in_pairs:
                all_stoats[group[::-1]].append(entry[2:])

        cnter: Counter = Counter()
        if in_pairs:
            cnter[stoat] = 1
        else:
            cnter.update(list(stoat))

        for _ in range(generations):
            next_gen: Counter = Counter()

            for group, cnt in cnter.items():
                rule: str = all_stoats[group][0]
                new_stoat: str = f"{group[0]}{rule}{group[1]}" if in_pairs else rule
                new_groups: list[str] = ["".join(x) for x in pairwise(new_stoat)] if in_pairs else list(new_stoat)

                for next_group, next_cnt in Counter(new_groups).items():
                    next_gen[next_group] += next_cnt * cnt

            cnter = next_gen

        return sum(cnter.values()) + in_pairs

    def part01(self) -> None:
        """Solution to Part 01."""
        print(f"Part 01: {self.evolve(stoat='AB', generations=7)}")

    def part02(self) -> None:
        """Solution to Part 02."""
        print(f"Part 02: {self.evolve(stoat='AB', generations=7, in_pairs=True)}")

    def part03(self) -> None:
        """Solution to Part 03."""
        print(f"Part 03: {self.evolve(stoat='AB', generations=21, in_pairs=True)}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
