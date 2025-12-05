from dataclasses import dataclass
from pathlib import Path


class DisjointRangeError(Exception): ...


@dataclass
class FreshRange:
    start: int
    end: int

    def __contains__(self, i: int) -> bool:
        return self.start <= i <= self.end

    def __lt__(self, other: "FreshRange") -> bool:
        if not isinstance(other, FreshRange):
            return NotImplemented
        return self.start < other.start

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __add__(self, other: "FreshRange") -> "FreshRange":
        if not isinstance(other, FreshRange):
            return NotImplemented

        # Check overlap/adjacency
        if max(self.start, other.start) <= min(self.end, other.end) + 1:
            return FreshRange(min(self.start, other.start), max(self.end, other.end))

        raise DisjointRangeError(f"Cannot merge {self} and {other}")


def merge_fresh_ranges(ranges: list[FreshRange]) -> list[FreshRange]:
    """
    Sorts and merges a list of ranges into their most unified form.
    """
    if not ranges:
        return []

    sorted_ranges = sorted(ranges)
    merged = []
    current_range = sorted_ranges[0]

    for next_range in sorted_ranges[1:]:
        try:
            current_range = current_range + next_range
        except DisjointRangeError:
            merged.append(current_range)
            current_range = next_range

    merged.append(current_range)
    return merged


@dataclass
class IngredientDatabase:
    fresh_ranges: list[FreshRange]
    inventory: set[int]

    def optimize_ranges(self):
        """Merges overlaps to ensure ranges are disjoint."""
        self.fresh_ranges = merge_fresh_ranges(self.fresh_ranges)

    def is_fresh(self, ingredient_id: int) -> bool:
        for fresh_range in self.fresh_ranges:
            if ingredient_id in fresh_range:
                return True
        return False

    @property
    def total_fresh_count(self) -> int:
        self.optimize_ranges()
        return sum(len(r) for r in self.fresh_ranges)


def parse_input(input_text: str) -> IngredientDatabase:
    fresh_range_lines, inventory_lines = input_text.split("\n\n")

    fresh_ranges = [
        FreshRange(int(start), int(stop))
        for start, stop in (
            fresh_range.split("-") for fresh_range in fresh_range_lines.splitlines()
        )
    ]
    inventory = set(int(_id) for _id in inventory_lines.splitlines())
    return IngredientDatabase(fresh_ranges, inventory)


def main(input_path: Path):
    input_text = input_path.read_text()
    db = parse_input(input_text)
    db.optimize_ranges()

    p1_result = 0
    for ingredient_id in db.inventory:
        if db.is_fresh(ingredient_id):
            p1_result += 1

    print(f"Part 1: {p1_result}")
    print(f"Part 2: {db.total_fresh_count}")
