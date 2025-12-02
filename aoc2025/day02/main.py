from pathlib import Path
from typing import Generator


def is_invalid_p1(number: int) -> bool:
    number_text = str(number)
    length = len(number_text)
    mid_point = length // 2
    return number_text[:mid_point] == number_text[mid_point:]


def is_invalid_p2(number: int) -> bool:
    number_text = str(number)
    length = len(number_text)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = number_text[:pattern_len]
            pattern_repeated = pattern * (length // pattern_len)
            if pattern_repeated == number_text:
                return True

    return False


def parse_input(input_text: str) -> Generator[int, None, None]:
    for _range in input_text.split(","):
        start, stop = _range.split("-")
        for number in range(int(start), int(stop) + 1):
            yield number


def main(input_path: Path):
    input_text = input_path.read_text().replace("\n", "")

    p1_result = 0
    p2_result = 0

    for number in parse_input(input_text):
        if is_invalid_p1(number):
            p1_result += number
        if is_invalid_p2(number):
            p2_result += number

    print(f"Part 1: {p1_result}")
    print(f"Part 2: {p2_result}")
