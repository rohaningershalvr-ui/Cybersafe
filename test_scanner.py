import tempfile
import unittest
from pathlib import Path

from scanner import scan_folder, sha256_file


class CyberSafeTests(unittest.TestCase):

    def test_sha256(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "hello.txt"
            file.write_text("hello", encoding="utf-8")

            self.assertEqual(
                sha256_file(file),
                "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
            )

    def test_scan_counts_files(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "hello.txt").write_text("hello")
            (folder / "demo.sh").write_text("test only")

            report = scan_folder(folder)

            self.assertEqual(report["files_found"], 2)
            self.assertEqual(report["files_flagged_for_review"], 1)

    def test_missing_folder_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "does-not-exist"

            with self.assertRaises(ValueError):
                scan_folder(missing)


if __name__ == "__main__":
    unittest.main()
