from pathlib import Path


def max_joltage(bank: str, k: int) -> str:
    """
    Finds the battery subsequence of length k that produces the highest
    joltage without rearranging the relative order in the bank.
    """
    # Base case: if we need 0 items, return empty string
    if k == 0:
        return ""

    # Base case: if we need items but bank is empty, this path is impossible
    if not bank:
        return None

    candidates = sorted(list(set(bank)), reverse=True)

    for best_battery in candidates:
        best_index = bank.find(best_battery)
        remaining_bank = bank[best_index + 1 :]

        # Assuming banks are over k elements, if the remaining string is shorter than what we need,
        # this candidate cannot possibly be the start of the best battery sequence.
        if len(remaining_bank) < k - 1:
            continue

        # Try to find the best sequence for the rest
        suffix_result = max_joltage(remaining_bank, k - 1)

        # If the recursive step returned a valid string (not None), we found our max.
        # Because we iterate candidates from largest to smallest, the first valid
        # path we find is guaranteed to be the maximum possible value.
        if suffix_result is not None:
            return best_battery + suffix_result

    # If no candidates lead to a solution
    return None


def main(input_path: Path):
    input_text = input_path.read_text()

    result_p1 = 0
    result_p2 = 0
    for bank in input_text.splitlines():
        result_p1 += int(max_joltage(bank, k=2))
        result_p2 += int(max_joltage(bank, k=12))

    print(f"Part 1: {result_p1}")
    print(f"Part 2: {result_p2}")
