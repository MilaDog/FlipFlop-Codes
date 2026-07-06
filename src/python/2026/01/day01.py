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

    @staticmethod
    def calculate_heating_cooling_time(current_temp: int, target_temp: int, perform_cooling: bool = False) -> int:
        """Perform heating or cooling of the coffee to determine the time needed to get the original coffee to the
        desired temperature.

        Args:
            current_temp (int): Current temperature of the coffee.
            target_temp (int): Target temperature of the coffee.
            perform_cooling (bool): Whether to perform cooling. Default is FALSE.

        Returns:
            int: Time take to get the original coffee to the desired temperature.
        """
        if not perform_cooling:
            return max(target_temp - current_temp, 0)

        diff: int = target_temp - current_temp
        return diff if diff > 0 else abs(diff) * 5

    def part01(self) -> None:
        """Solution to Part 01."""
        tlt: int = sum(Solution.calculate_heating_cooling_time(current_temp=line, target_temp=60) for line in self.data)
        print(f"Part 01: {tlt}")

    def part02(self) -> None:
        """Solution to Part 02."""
        tlt: int = sum(
            Solution.calculate_heating_cooling_time(current_temp=line, target_temp=60, perform_cooling=True)
            for line in self.data
        )
        print(f"Part 02: {tlt}")

    def part03(self) -> None:
        """Solution to Part 03."""
        lngth: int = len(self.data) // 2

        coffee_temps: list[int] = self.data[:lngth]
        preferred_temps: list[int] = self.data[lngth:]

        tlt: int = sum(
            Solution.calculate_heating_cooling_time(current_temp=t1, target_temp=t2, perform_cooling=True)
            for t1, t2 in zip(coffee_temps, preferred_temps)
        )
        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
