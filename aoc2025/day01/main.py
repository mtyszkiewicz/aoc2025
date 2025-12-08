from dataclasses import dataclass
from typing import Literal

from typing_extensions import Self

DIAL_MAX = 100


@dataclass
class Instruction:
    rotate_direction: Literal["L", "R"]
    distance: int

    def parse(line: str) -> Self:
        return Instruction(rotate_direction=line[0], distance=int(line[1:]))


def parse_input(input_text: str) -> list[Instruction]:
    return [Instruction.parse(line) for line in input_text.splitlines()]


@dataclass
class SafeDial:
    state: int = 50
    click_count: int = 0

    def rotate(self, instr: Instruction):
        if instr.rotate_direction == "L":
            dx = -1
        if instr.rotate_direction == "R":
            dx = 1

        for _ in range(instr.distance):
            self.state = (self.state + dx) % DIAL_MAX
            if self.state == 0:
                self.click_count += 1


def main(input_text: str):
    dial = SafeDial()

    zero_stops = 0

    instructions = parse_input(input_text)
    for instr in instructions:
        dial.rotate(instr)

        if dial.state == 0:
            zero_stops += 1

    print(f"Part 1: {zero_stops}")
    print(f"Part 2: {dial.click_count}")