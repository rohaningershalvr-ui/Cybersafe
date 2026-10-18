import unittest

from baseline import compare_baselines


class BaselineTests(unittest.TestCase):

    def test_added_file(self):
        old = {"hello.txt": "abc"}
        new = {"hello.txt": "abc", "new.txt": "xyz"}

        result = compare_baselines(old, new)

        self.assertEqual(result["added"], ["new.txt"])
        self.assertEqual(result["modified"], [])
        self.assertEqual(result["removed"], [])

    def test_modified_file(self):
        old = {"hello.txt": "old-hash"}
        new = {"hello.txt": "new-hash"}

        result = compare_baselines(old, new)

        self.assertEqual(result["modified"], ["hello.txt"])

    def test_removed_file(self):
        old = {"hello.txt": "abc", "old.txt": "xyz"}
        new = {"hello.txt": "abc"}

        result = compare_baselines(old, new)

        self.assertEqual(result["removed"], ["old.txt"])

    def test_unchanged_files(self):
        old = {"hello.txt": "abc"}
        new = {"hello.txt": "abc"}

        result = compare_baselines(old, new)

        self.assertEqual(result["added"], [])
        self.assertEqual(result["modified"], [])
        self.assertEqual(result["removed"], [])


if __name__ == "__main__":
    unittest.main()
