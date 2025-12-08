import importlib
import os
import signal
import sys
import tempfile
from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def get_input_path(args, day_num):
    """
    Determines the input source based on arguments and stdin.
    Yields a Path object to be used by the puzzle solution.
    """
    # 1. Explicit file argument via -f/--file
    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: File not found: {path}")
            sys.exit(1)
        yield path
        return

    # 2. Piped input (stdin)
    # Check if stdin is NOT a terminal (implies data is being piped in)
    if not sys.stdin.isatty():
        fd, temp_path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                # Read all content from stdin pipe
                tmp.write(sys.stdin.read())
            yield Path(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        return

    # 3. Internal default (input.txt or example.txt)
    base_dir = Path(__file__).parent / f"day{day_num}" / "input"
    filename = "example.txt" if args.example else "input.txt"
    internal_path = base_dir / filename

    if not internal_path.exists():
        print(f"Error: Internal input not found: {internal_path}")
        sys.exit(1)
        
    yield internal_path


def main():
    # Handle BrokenPipeError (e.g., when piping output to `head`) without crashing
    # This is Unix-specific; Windows ignores SIGPIPE.
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    argparser = ArgumentParser(prog="aoc")
    argparser.add_argument("day", type=str, help="Day number (e.g., 1 or 01)")
    argparser.add_argument("-x", "--example", action="store_true", help="Use internal example input")
    argparser.add_argument("-f", "--file", type=str, help="Path to custom input file")
    
    args = argparser.parse_args()
    
    day_num = args.day.zfill(2)
    
    # Try importing as a package (for uvx/installed mode) first
    module_name = f"aoc2025.day{day_num}.main"
    
    try:
        day_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        # Fallback for local development if not running as an installed package
        try:
            module_name = f"day{day_num}.main"
            day_module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            print(f"Error: Could not find module for Day {day_num} ({module_name})")
            sys.exit(1)

    with get_input_path(args, day_num) as input_path:
        day_module.main(input_path.read_text())


if __name__ == "__main__":
    main()