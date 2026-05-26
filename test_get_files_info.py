import unittest
from functions.get_files_info import get_files_info

class TestGetFiles(unittest.TestCase):
    def test_current_dir(self) -> None:
        result = get_files_info("calculator", ".")
        self.assertIn("Success", result)

    def test_bin_dir(self) -> None:
        result = get_files_info("calculator", "/bin")
        self.assertIn("Error", result)
        self.assertIn("Cannot list \"/bin\"", result)

    def test_parent_dir(self) -> None:
        result = get_files_info("calculator", "../")
        self.assertIn("Error", result)
        self.assertIn("Cannot list \"../\"", result)

    def test_no_dir(self) -> None:
        result = get_files_info("calculator", "main.py")
        self.assertIn("Error", result)
        self.assertIn("is not a directory", result)



    


if __name__ == "__main__":
    unittest.main()
