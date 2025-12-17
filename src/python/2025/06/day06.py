import math

type Coords = tuple[int, ...]


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[Coords]):
        self.data: list[Coords] = data
        self.sky_size: tuple[int, int] = (1000, 1000)
        self.frame_size: tuple[int, int] = (500, 500)

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        data: list[Coords] = []

        with open("./inputs/flipflopcodes/2025/06/input.txt") as file:
            for line in file.readlines():
                data.append(tuple(map(int, line.strip().split(","))))

        return cls(data=data)

    def determine_cycle_length(self, dx: int, dy: int) -> int:
        """Determine the cycle length of the offsets within the given sky. Used to minimise the number of total
        iterations that are needed to change a bird's position, by exploiting the occurrence of cycles when performing
        the multiple bird position updates.

        Args:
            dx (int): X offset.
            dy (int): Y offset.

        Returns:
            int: Size of cycle within the given skybox.
        """
        dx %= self.sky_size[0]
        dy %= self.sky_size[1]

        if dx == 0 and dy == 0:
            return 1

        x_period: int = self.sky_size[0] // math.gcd(dx, self.sky_size[0]) if dx != 0 else 1
        y_period: int = self.sky_size[1] // math.gcd(dy, self.sky_size[1]) if dy != 0 else 1

        return (x_period * y_period) // math.gcd(x_period, y_period)

    def update_bird_position(self, initial_position: Coords, offset: Coords, times: int) -> Coords:
        """Determine the final position of the bird from the `initial_position` after a given number of `times`.

        Args:
            initial_position (Coords): Initial position of the bird.
            offset (Coords): Speed of the bird.
            times (int): Number of iterations to perform.

        Returns:
            Coords: Final bird's position.
        """
        x, y = initial_position
        dx, dy = offset

        times %= self.determine_cycle_length(dx=dx, dy=dy)

        new_x = (x + dx * times) % self.sky_size[0]
        new_y = (y + dy * times) % self.sky_size[1]

        return new_x, new_y

    def is_within_frame_bounds(self, bird_position: Coords) -> bool:
        """Determine whether the bird is within the frame for the photo or not.

        Args:
            bird_position (Coords): Position of the bird.

        Returns:
            bool: If the bird is within frame.
        """
        x, y = bird_position

        x_padding: int = (self.sky_size[0] - self.frame_size[0]) // 2
        y_padding: int = (self.sky_size[1] - self.frame_size[1]) // 2
        return x_padding <= x < (self.sky_size[0] - x_padding - 1) and y_padding <= y < (
            self.sky_size[1] - y_padding - 1
        )

    def solve(self, elapse_time: int, num_photos: int) -> int:
        """Solve the problem.

        Args:
            elapse_time (int): Elapse time of the bird moving in the grid between photos.
            num_photos (int): Number of photos to take.

        Returns:
            int: Total number of birds seen in each photo.
        """
        tlt: int = 0

        birds: list[Coords] = [(0, 0) for _ in range(len(self.data))]
        for _ in range(num_photos):
            cnter: int = 0

            new_bird_positions: list[Coords] = []
            for bird, offset in zip(birds, self.data):
                new_position: Coords = self.update_bird_position(
                    initial_position=bird, offset=offset, times=elapse_time
                )
                new_bird_positions.append(new_position)
                cnter += self.is_within_frame_bounds(bird_position=new_position)

            tlt += cnter
            birds = new_bird_positions

        return tlt


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    print(f"Part 01: {sol.solve(elapse_time=100, num_photos=1)}")
    print(f"Part 02: {sol.solve(elapse_time=3600, num_photos=1000)}")
    print(f"Part 02: {sol.solve(elapse_time=31556926, num_photos=1000)}")
