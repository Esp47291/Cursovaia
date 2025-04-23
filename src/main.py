
import argparse
from pathlib import Path

from .views import index

def main() -> None:
    parser = argparse.ArgumentParser(description="Coursework 1 demo CLI")
    parser.add_argument("--datetime", default="2023-12-15 15:30:00", help="Datetime 'YYYY-MM-DD HH:MM:SS'")
    parser.add_argument("--file", default=str(Path(__file__).resolve().parent.parent / "data" / "operations.xlsx"))
    args = parser.parse_args()

    print(index(args.datetime, args.file))


if __name__ == "__main__":
    main()
