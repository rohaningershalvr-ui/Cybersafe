import argparse
import json
from pathlib import Path

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def main():
    parser = argparse.ArgumentParser(
        description="Compare file-integrity baselines."
    )
    parser.add_argument("old", help="Original baseline JSON")
    parser.add_argument("new", help="Latest baseline JSON")
    args = parser.parse_args()

    try:
        old = json.loads(Path(args.old).read_text(encoding="utf-8"))
        new = json.loads(Path(args.new).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(str(error))

    old_names = set(old)
    new_names = set(new)

    added = sorted(new_names - old_names)
    removed = sorted(old_names - new_names)
    modified = sorted(
        name for name in old_names & new_names
        if old[name] != new[name]
    )

    print()
    print(CYAN + BOLD + "=" * 42 + RESET)
    print(CYAN + BOLD + "      CYBERSAFE CHANGE REPORT" + RESET)
    print(CYAN + BOLD + "=" * 42 + RESET)

    sections = [
        ("ADDED FILES", added, GREEN),
        ("MODIFIED FILES", modified, YELLOW),
        ("REMOVED FILES", removed, RED),
    ]

    for title, files, color in sections:
        print(f"\n{BOLD}{title}{RESET} ({len(files)})")
        if files:
            for name in files:
                print(f"  {color}+ {name}{RESET}")
        else:
            print("  None")

    print("\nA change is not automatically a security incident.")
    print()


if __name__ == "__main__":
    main()
