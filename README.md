# Advent of Code 2025

Python solutions for [Advent of Code 2025](https://adventofcode.com/2025).

## Usage

Run solutions on your own puzzle input using [`uvx`](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# Run Day 1 with input from clipboard
pbpaste | uvx --from git+https://github.com/mtyszkiewicz/aoc2025 aoc 1

# Run Day 1 with a specific file
uvx --from git+https://github.com/mtyszkiewicz/aoc2025 aoc 1 -f input.txt
```

## Local Development
```bash
# Show all available options
uv run aoc --help

# Run Day 1 (uses internal input)
uv run aoc 1

# Run Day 1 with example input
uv run aoc 1 -x
```