from collections import defaultdict
from pathlib import Path


def main(input_path: Path):
    input_text = input_path.read_text()

    total_splits = 0
    beams = defaultdict(int)
    for y, line in enumerate(input_text.splitlines()):
        if y == 0:
            beams[line.find("S")] += 1
            continue
        
        for x, c in enumerate(line):
            if c == "^" and beams[x] != 0:
                beams[x - 1] += beams[x]
                beams[x + 1] += beams[x]
                beams[x] = 0
                total_splits += 1

    print(f"Part 1: {total_splits}")
    print(f"Part 2: {sum(beams.values())}")