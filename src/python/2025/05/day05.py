from collections import defaultdict


class Solution:
    """Solution for the problem."""

    def __init__(self, data: str, train_lines: dict[str, list[int]], endpoints: dict[int, int]):
        self.data: str = data
        self.train_lines: dict[str, list[int]] = train_lines
        self.endpoints: dict[int, int] = endpoints

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        train_lines: dict[str, list[int]] = defaultdict(list)
        endpoints: dict[int, int] = {}
        data: str = ""

        with open("./inputs/flipflopcodes/2025/05/input.txt") as file:
            data = file.read().strip()
            for i, char in enumerate(data):
                train_lines[char].append(i)

                if len(train_lines[char]) == 2:
                    start, end = train_lines[char]
                    endpoints[start] = end
                    endpoints[end] = start

        return cls(data=data, train_lines=train_lines, endpoints=endpoints)

    def solve(self) -> None:
        """Solution to Part 01, 02, and 03."""
        tlt1: int = 0
        tlt2: int = 0

        unseen_trains: list[str] = [k for k in self.train_lines.keys()]

        pos: int = 0
        while pos < len(self.data):
            train: str = self.data[pos]

            if train in unseen_trains:
                unseen_trains.remove(train)

            distance: int = self.train_lines[train][1] - self.train_lines[train][0]
            tlt1 += distance
            tlt2 += distance * (1, -1)[train.isupper()]

            pos = self.endpoints[pos] + 1

        print(f"Part 01: {tlt1}")
        print(f"Part 02: {"".join(unseen_trains)}")
        print(f"Part 03: {tlt2}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.solve()
