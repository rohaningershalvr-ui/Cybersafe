import hashlib
import json
from pathlib import Path


def fingerprint(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def build_baseline(folder):
    root = Path(folder).expanduser().resolve()

    if not root.is_dir():
        raise ValueError("Folder does not exist.")

    baseline = {}

    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            try:
                baseline[str(path.relative_to(root))] = fingerprint(path)
            except OSError as error:
                print(f"Skipped {path}: {error}")

    return baseline


def compare_baselines(old, new):
    old_names = set(old)
    new_names = set(new)

    return {
        "added": sorted(new_names - old_names),
        "removed": sorted(old_names - new_names),
        "modified": sorted(
            name for name in old_names & new_names
            if old[name] != new[name]
        ),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create or compare a local file-integrity baseline."
    )
    parser.add_argument("folder", help="Folder you own or are authorized to inspect")
    parser.add_argument(
        "--compare",
        help="Path to an earlier baseline JSON file"
    )
    parser.add_argument(
        "--save",
        default="baseline.json",
        help="Where to save the new baseline"
    )
    args = parser.parse_args()

    try:
        current = build_baseline(args.folder)

        if args.compare:
            old = json.loads(
                Path(args.compare).read_text(encoding="utf-8")
            )
            print(json.dumps(compare_baselines(old, current), indent=2))

        Path(args.save).write_text(
            json.dumps(current, indent=2),
            encoding="utf-8"
        )
        print(f"Baseline saved to {args.save}")
        print(f"Files recorded: {len(current)}")

    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
