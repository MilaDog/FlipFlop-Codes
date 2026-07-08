import re


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2026/03/input.txt") as file:
            values: list[str] = [line.strip() for line in file.readlines()]

        return cls(data=values)

    def find_max_consecutive_characters(self, password: str) -> tuple[str, int]:
        """Find the longest consecutive character string and return the character and its length.

        Args:
            password (str): String to search.

        Returns:
            tuple[str, int]: Found character and its length.
        """
        password_lngth: int = len(password)
        max_cnt: int = 0
        ltr: str = password[0]

        cnter: int = 0
        while cnter < password_lngth:
            cnt: int = 1

            while cnter + 1 < password_lngth and password[cnter] == password[cnter + 1]:
                cnter += 1
                cnt += 1

            if cnt > max_cnt:
                max_cnt = cnt
                ltr = password[cnter]

            cnter += 1

        return ltr, max_cnt

    def get_base_password_score(self, password: str) -> int:
        """Get the base score for the given password.

        Args:
            password (str): Password to evaluate.

        Returns:
            int: Base score of the password.
        """
        return sum(
            bool(re.search(pattern, password))
            for pattern in (
                r"[a-z]",
                r"[A-Z]",
                r"\d",
            )
        )

    def determine_score(self, password: str) -> int:
        """Determine the overall score of the password.

        Args:
            password (str): Password to evaluate.

        Returns:
            int: Overall password score.
        """
        score: int = self.get_base_password_score(password=password)

        # digit checking
        has_digits: set[int] = set(map(int, list(re.findall(r"\d", password))))
        if len(has_digits) == 1 and 7 in has_digits:
            score += 7

        # consecutive character checking
        cc_password: tuple[str, int] = self.find_max_consecutive_characters(password=password)
        if cc_password[-1] >= 3:
            score += cc_password[-1] ** 2

        # colour checking
        has_colour: list[str] = list(re.findall(r"(red|green|blue)", password))
        score *= 3 if has_colour else 1

        return score * len(password)

    def part01(self) -> None:
        """Solve Part 01."""
        ans: str = ""
        tlt: int = 0

        for password in self.data:
            score: int = self.get_base_password_score(password=password) * len(password)

            if score >= tlt:
                tlt = score
                ans = password

        print(f"Part 01: {ans}")

    def part02(self) -> None:
        """Solve Part 02."""
        ans: str = ""
        tlt: int = 0

        for password in self.data:
            score: int = self.determine_score(password=password)

            if score >= tlt:
                tlt = score
                ans = password

        print(f"Part 02: {ans} ({tlt})")

    def part03(self) -> None:
        """Solve Part 03."""
        ltrs: str = "abcdefghijklmnopqrstuvwxyz"
        ltrs += ltrs.upper()
        ltrs += "0123456789"

        tlt: int = max([sum(self.determine_score(password=password + ltr) for password in self.data) for ltr in ltrs])

        print(f"Part 03: {tlt}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
