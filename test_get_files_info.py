import unittest
from functions.get_files_info import get_files_info

class TestGetFiles(unittest.TestCase):
    def test_current_dir(self) -> None:
        result = get_files_info("calculator", ".")
        # print("Result for current directory:")
        # print("   ", result)
        self.assertIn("main.py", result)
        self.assertIn("tests.py", result)
        self.assertIn("pkg", result)
        self.assertIn("is_dir=True", result)
        self.assertIn("is_dir=False", result)

    def test_pkg(self) -> None:
        result = get_files_info("calculator", "pkg")
        # print("Result for 'pkg' directory")
        # print("   ", result)
        self.assertIn("calculator.py", result)
        self.assertIn("render.py", result)

    def test_bin_dir(self) -> None:
        result = get_files_info("calculator", "/bin")
        # print("Result for '/bin' directory")
        # print("   ", result)
        self.assertIn("Error", result)
        self.assertIn("Cannot list \"/bin\"", result)

    def test_parent_dir(self) -> None:
        result = get_files_info("calculator", "../")
        # print("Result for '../' directory")
        # print("   ", result)
        self.assertIn("Error", result)
        self.assertIn("Cannot list \"../\"", result)

    def test_no_dir(self) -> None:
        result = get_files_info("calculator", "main.py")
        # print("Result for main.py file")
        # print("   ", result)
        self.assertIn("Error", result)
        self.assertIn("is not a directory", result)

if __name__ == "__main__":
    unittest.main()
