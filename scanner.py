import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# File types that deserve review, not automatic accusations.
REVIEW_EXTENSIONS = {
    ".apk", ".bat", ".cmd", ".com", ".exe",
    ".js", ".ps1", ".scr", ".sh", ".vbs"
}

def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()

def scan_folder(folder):
    folder = Path(folder).expanduser().resolve()

    if not folder.is_dir():
        raise ValueError("The supplied path is not a directory.")

    results = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue

        try:
            results.append({
                "file": str(path.relative_to(folder)),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "review_required": (
                    path.suffix.lower() in REVIEW_EXTENSIONS
                ),
            })
        except (OSError, PermissionError) as error:
            results.append({
                "file": str(path.relative_to(folder)),
                "error": str(error),
            })

    return {
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "folder": str(folder),
        "files_found": len(results),
        "files_flagged_for_review": sum(
            item.get("review_required", False)
            for item in results
        ),
        "results": results,
        "note": (
            "Extension flags are not proof of malware. "
            "SHA-256 identifies file content; it does not prove safety."
        ),
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python scanner.py FOLDER_PATH")
        raise SystemExit(2)

    try:
        report = scan_folder(sys.argv[1])
    except (ValueError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)

    output = Path("cybersafe-report.json")
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Files found: {report['files_found']}")
    print(f"Flagged for review: {report['files_flagged_for_review']}")
    print(f"Report saved: {output.resolve()}")

if __name__ == "__main__":
    main()
