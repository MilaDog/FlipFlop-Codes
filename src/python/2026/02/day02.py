from dataclasses import dataclass


@dataclass
class RoboticSegment:
    """Representation of a robotic wall segment."""

    id_: int
    pos: int
    temp: int


class Wall:
    """Representation of the wall of robotic segments."""

    def __init__(self, lngth: int):
        self.segments: list[RoboticSegment] = [RoboticSegment(id_=i + 1, pos=i, temp=0) for i in range(lngth)]
        self.highest_temp: int = 0

    def heat_up_wall_segment(self, laser_pos: int) -> None:
        """Heat up the robotic wall segment at the given laser position.

        Args:
            laser_pos (int): Position of the laser.
        """
        target_robotic_segment: RoboticSegment = list(filter(lambda rs: rs.pos == laser_pos, self.segments))[0]
        target_robotic_segment.temp += 1

        if target_robotic_segment.temp > self.highest_temp:
            self.highest_temp = target_robotic_segment.temp

    def get_hottest_wall_segment_with_lowest_id(self) -> RoboticSegment:
        """Get the robotic wall segment with the highest temperature. Choose the wall segment with the lowest ID if
        multiple share the same temperature.

        Returns:
            RoboticSegment: Found robotic wall segment.
        """
        filtered_segments: list[RoboticSegment] = list(filter(lambda rs: rs.temp == self.highest_temp, self.segments))
        return sorted(filtered_segments, key=lambda rs: rs.id_)[0]

    def move_all_segments(self, direction: int, wrap: bool = True) -> None:
        """Move all robotic wall segments in the target direction.

        Args:
            direction (int): Direction to move the wall segments.
            wrap (bool): Whether to wrap around. Default is TRUE.
        """
        for seg in self.segments:
            seg.pos += direction

            if wrap:
                seg.pos %= len(self.segments)


class Solution:
    """Solution for the problem."""

    def __init__(self, data: list[str]):
        self.data: list[str] = data
        self.moves: dict[str, int] = {"<": -1, ">": 1}
        self.lngth: int = 100

    @classmethod
    def parse(cls) -> "Solution":
        """Parse the problem input file."""
        with open("./inputs/flipflopcodes/2026/02/input.txt") as file:
            values: list[str] = list(file.read().strip())

        return cls(data=values)

    def part01(self) -> None:
        """Solve Part 01."""
        pos_laser: int = 0
        wall: Wall = Wall(lngth=self.lngth)

        for move in self.data:
            pos_laser = (pos_laser + self.moves[move]) % self.lngth
            wall.heat_up_wall_segment(laser_pos=pos_laser)

        hottest_segment: RoboticSegment = wall.get_hottest_wall_segment_with_lowest_id()
        print(f"Part 01: {hottest_segment.id_ * hottest_segment.temp}")

    def part02(self) -> None:
        """Solve Part 02."""
        pos_laser: int = 0
        wall: Wall = Wall(lngth=self.lngth)
        segment_01: RoboticSegment = wall.segments[0]

        for laser_move, robot_move in zip(self.data, self.data[::-1]):
            pos_laser = (pos_laser + self.moves[laser_move]) % self.lngth
            segment_01.pos = (segment_01.pos + self.moves[robot_move]) % self.lngth

            if segment_01.pos == pos_laser:
                segment_01.temp += 1

        print(f"Part 02: {segment_01.temp}")

    def part03(self) -> None:
        """Solve Part 03."""
        pos_laser: int = 0
        wall: Wall = Wall(lngth=self.lngth)

        for laser_move, robot_move in zip(self.data, self.data[::-1]):
            pos_laser = (pos_laser + self.moves[laser_move]) % self.lngth
            wall.move_all_segments(direction=self.moves[robot_move])
            wall.heat_up_wall_segment(laser_pos=pos_laser)

        hottest_segment: RoboticSegment = wall.get_hottest_wall_segment_with_lowest_id()
        print(f"Part 03: {hottest_segment.id_ * hottest_segment.temp}")


if __name__ == "__main__":
    sol: Solution = Solution.parse()
    sol.part01()
    sol.part02()
    sol.part03()
