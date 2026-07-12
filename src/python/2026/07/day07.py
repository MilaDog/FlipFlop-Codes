from collections import deque
from dataclasses import dataclass, field


@dataclass
class Snake:
    """Representation of the Ross' snake."""

    current_head_position: tuple[int, int] = (0, 0)
    body: deque[tuple[int, int]] = field(default_factory=deque)
    sushi_eaten: int = 0
    self_eaten_count: int = 0

    def update_position(self, move: str) -> None:
        """Update the snake's position according to the given move.

        Args:
            move (str): Move made by the snake.
        """
        dx, dy = {"<": (-1, 0), ">": (1, 0), "^": (0, 1), "v": (0, -1)}[move]
        x, y = self.current_head_position

        self.current_head_position = (x + dx, y + dy)

    def head_occupies_body(self) -> bool:
        """Whether the current head position is on the body of the snake."""
        return self.current_head_position in self.body

    def move(self) -> None:
        """Move the snake."""
        self.body.popleft()

    def grow(self) -> None:
        """Add the current head position to the snake's body."""
        self.body.append(self.current_head_position)

    def size(self) -> int:
        """Get the size of the snake."""
        return len(self.body)

    def eat_self(self) -> None:
        """Snake ate self, so remove trailing body."""
        self.self_eaten_count += 1

        for _ in range(self.body.index(self.current_head_position) + 2):
            self.body.popleft()


class Solution:
    """Solution for the problem."""

    def __init__(self, moves: list[str], sushi_locations: list[tuple[int, int]]):
        self.moves: list[str] = moves
        self.sushi_locations: list[tuple[int, int]] = sushi_locations

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        moves: list[str] = []
        sushi_locations: list[tuple[int, int]] = []

        with open("./inputs/flipflopcodes/2026/input07.txt") as file:
            s1, s2 = file.read().split("\n\n")

            moves += list(s1.strip())

            for pos in s2.strip().split("\n"):
                x, y = pos.strip().split(",")
                sushi_locations.append((int(x), int(y)))

        return cls(moves=moves, sushi_locations=sushi_locations)

    def part01(self) -> None:
        """Solution to Part 01."""
        snake: Snake = Snake()

        sushi = iter(self.sushi_locations)
        curr_sushi: tuple[int, int] = next(sushi)

        for move in self.moves[: len(self.moves) // 2]:
            snake.update_position(move)

            if snake.current_head_position == curr_sushi:
                snake.sushi_eaten += 1
                curr_sushi = next(sushi)

        print(f"Part 01: {snake.sushi_eaten}")

    def part02(self) -> None:
        """Solution to Part 02."""
        snake: Snake = Snake()
        snake.body.append(snake.current_head_position)

        sushi = iter(self.sushi_locations)
        curr_sushi: tuple[int, int] = next(sushi)

        for move in self.moves:
            snake.update_position(move)

            if snake.current_head_position == curr_sushi:
                curr_sushi = next(sushi, (-1, -1))

            else:
                snake.move()

                if snake.head_occupies_body():
                    break

            snake.grow()

        print(f"Part 02: {snake.size() + 1}")

    def part03(self) -> None:
        """Solution to Part 03."""
        snake: Snake = Snake()
        snake.body.append(snake.current_head_position)

        sushi = iter(self.sushi_locations)
        curr_sushi: tuple[int, int] = next(sushi)

        for move in self.moves:
            snake.update_position(move)

            if snake.current_head_position == curr_sushi:
                curr_sushi = next(sushi, (-1, -1))

            else:
                snake.move()

                if snake.head_occupies_body():
                    snake.eat_self()

            snake.grow()

        print(f"Part 03: {snake.size() * snake.self_eaten_count}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
