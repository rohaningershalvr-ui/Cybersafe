import json
import sys
from pathlib import Path

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def main():
    report_path = Path(
        sys.argv[1] if len(sys.argv) > 1
        else "cybersafe-report.json"
    )

    if not report_path.is_file():
        print(f"Report not found: {report_path}")
        print("Run scanner.py first to generate a report.")
        raise SystemExit(1)

    report = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    print()
    print(CYAN + BOLD + "=" * 44 + RESET)
    print(CYAN + BOLD + "          CYBERSAFE DASHBOARD" + RESET)
    print(CYAN + BOLD + "=" * 44 + RESET)

    print(f"\nFolder: {report.get('folder', 'Unknown')}")
    print(f"Files scanned: {report.get('files_found', 0)}")

    flagged = report.get("files_flagged_for_review", 0)
    color = YELLOW if flagged else GREEN
    print(color + f"Files flagged for review: {flagged}" + RESET)

    print("\n" + BOLD + "FILE DETAILS" + RESET)
    print("-" * 44)

    for item in report.get("results", []):
        if "error" in item:
            print(RED + f"[ERROR] {item['file']}" + RESET)
            continue

        if item.get("review_required"):
            status = YELLOW + "[REVIEW]" + RESET
        else:
            status = GREEN + "[OK]" + RESET

        print(f"{status} {item['file']}")
        print(f"   Size: {item['size_bytes']} bytes")
        print(f"   SHA-256: {item['sha256']}")

    print("\n" + CYAN + "=" * 44 + RESET)
    print("Extension flags are indicators, not malware verdicts.")
    print()


if __name__ == "__main__":
    main()
