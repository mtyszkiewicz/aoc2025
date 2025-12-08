from typing import Generator, Literal

Value = Literal[".", "@", "x"]
Point = tuple[int, int]
Grid = dict[Point, Value]

NEIGHBORS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def parse_input(input_text: str) -> Grid:
    return {
        (x, y): c
        for y, line in enumerate(input_text.splitlines())
        for x, c in enumerate(line)
    }


def neighbours(grid: Grid, pos: Point) -> Generator[Value, None, None]:
    x, y = pos
    for dx, dy in NEIGHBORS_8:
        p = (x + dx, y + dy)
        if p in grid:
            yield grid[p]


def find_papers_to_remove(grid: Grid) -> list[Point]:
    to_remove = []
    for pos, val in grid.items():
        if val == "@":
            neighboring_papers_count = sum(n == "@" for n in neighbours(grid, pos))
            if neighboring_papers_count < 4:
                to_remove.append(pos)

    return to_remove


def main(input_text: str):
    grid = parse_input(input_text)

    total_removed = 0
    while True:
        to_remove = find_papers_to_remove(grid)
        if len(to_remove) == 0:
            break

        for pos in to_remove:
            grid[pos] = "x"

        if total_removed == 0:
            print(f"Part 1: {len(to_remove)}")

        total_removed += len(to_remove)

    print(f"Part 2: {total_removed}")
