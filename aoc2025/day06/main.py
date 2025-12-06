import operator
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import pairwise
from pathlib import Path


@dataclass
class Operation:
    op: str
    start: int
    end: int


def parse_operations(line: str):
    results = []
    operation_matches = re.finditer(r"(\+|\*)", line)
    operation_pairs = list(pairwise(operation_matches))
    for curr_match, next_match in operation_pairs:
        results.append(
            Operation(
                op=curr_match.group(),
                start=curr_match.start(),
                end=next_match.end() - 2,
            )
        )
    results.append(
        Operation(
            op=operation_pairs[-1][1].group(),
            start=operation_pairs[-1][1].start(),
            end=len(line),
        )
    )
    return results


def parse_values(value_lines: list[str], operations: list[Operation]):
    columns = defaultdict(list)
    for i, op in enumerate(operations):
        for line in value_lines:
            columns[i].append(line[op.start : op.end])
    return columns.values()


def evaluate_part_1(operations: list[Operation], values: list[list[str]]):
    grand_total = 0
    for operation, numbers in zip(operations, values):
        numbers = [int(x) for x in numbers]
        if operation.op == "+":
            result = reduce(operator.add, numbers)
        if operation.op == "*":
            result = reduce(operator.mul, numbers)
        grand_total += result

    return grand_total


def evaluate_part_2(operations: list[Operation], values: list[list[str]]):
    grand_total = 0
    for operation, numbers in zip(operations, values):
        # organize vertically
        numbers = [
            int(reduce(operator.add, [n[i] for n in numbers]))
            for i in range(len(numbers[0]))
        ]

        numbers = [int(x) for x in numbers]
        if operation.op == "+":
            result = reduce(operator.add, numbers)
        if operation.op == "*":
            result = reduce(operator.mul, numbers)
        grand_total += result

    return grand_total


def main(input_path: Path):
    input_text = input_path.read_text()
    lines = input_text.splitlines()
    ops = parse_operations(lines[-1])
    values = parse_values(lines[:-1], ops)

    print(f"Part 1: {evaluate_part_1(ops, values)}")
    print(f"Part 2: {evaluate_part_2(ops, values)}")
