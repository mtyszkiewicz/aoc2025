import importlib
import sys
from argparse import ArgumentParser
from pathlib import Path


def main():
    argparser = ArgumentParser(prog="aoc")
    argparser.add_argument("-x", "--example", action="store_true")
    argparser.add_argument("day", type=str, help="Day number")
    args = argparser.parse_args()
    
    day_num = args.day.zfill(2)
    module_name = f"aoc2025.day{day_num}.main"
    
    input_dir = Path(__file__).parent / f"day{day_num}" / "input"
    if args.example:
        input_path = input_dir / "example.txt"
    else:
        input_path = input_dir / "input.txt"
    
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)
    
    day_module = importlib.import_module(module_name)
    day_module.main(input_path)
    

if __name__ == "__main__":
    main()