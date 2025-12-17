from functools import cache


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2025/02/input.txt") as file:
            values: list[str] = list(file.read().strip())

        return cls(data=values)

    @cache
    def fib(self, n: int) -> int:
        """Determine the Fibonacci value of `n`.

        Args:
            n (int): nth Fibonacci Sequence to calculate.

        Returns:
            int: Fibonacci result.
        """
        if n < 0:
            raise ValueError(f"Value has to be positive, got {n}")

        if n == 0 or n == 1:
            return n
        return self.fib(n - 1) + self.fib(n - 2)

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = 0
        curr: int = 0

        for action in self.data:
            match action:
                case "^":
                    curr += 1
                case "v":
                    curr -= 1
                case _:
                    raise ValueError(f"Unknown action: {action}")

            tlt = max(tlt, curr)

        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = 0
        curr: int = 0

        cnter_up: int = 0
        cnter_down: int = 0

        for action in self.data:
            match action:
                case "^":
                    cnter_down = 0
                    cnter_up += 1
                    curr += cnter_up
                case "v":
                    cnter_up = 0
                    cnter_down += 1
                    curr -= cnter_down
                case _:
                    raise ValueError(f"Unknown action: {action}")

            tlt = max(tlt, curr)

        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        tlt: int = 0
        curr: int = 0

        cnter_up: int = 0
        cnter_down: int = 0

        for action in self.data:
            match action:
                case "^":
                    cnter_up += 1

                    if cnter_down != 0:
                        curr -= self.fib(n=cnter_down)
                        cnter_down = 0

                case "v":
                    cnter_down += 1

                    if cnter_up != 0:
                        curr += self.fib(n=cnter_up)
                        cnter_up = 0

                case _:
                    raise ValueError(f"Unknown action: {action}")

            tlt = max(tlt, curr)

        else:
            if cnter_up != 0:
                curr += self.fib(n=cnter_up)

            if cnter_down != 0:
                curr -= self.fib(n=cnter_down)

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
