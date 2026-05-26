import unittest
from config import MAX_CHARS
from functions.get_file_content import get_file_content

LEN_EXTRA_MSG_TRUNCATED: int = 51

class TestGetFileContent(unittest.TestCase):
    def test_lorem(self) -> None:
        result = get_file_content("calculator", "lorem.txt")
        # print(f"lorem.txt length: {len(result)}")
        # print(f"lorem.txt truncated: {'truncated' in result}")
        self.assertTrue(len(result) > 0)
        self.assertEqual(MAX_CHARS + LEN_EXTRA_MSG_TRUNCATED, len(result))
        self.assertIn("truncated", result)
    
    def test_calculator_main(self) -> None:
        result = get_file_content("calculator", "main.py")
        # print(f"main.py length: {len(result)}")
        # print("Result of main.py:\n", result)
        self.assertTrue(len(result) > 0)

    def test_pkg_calculator(self) -> None:
        result = get_file_content("calculator", "pkg/calculator.py")
        # print(f"main.py length: {len(result)}")
        # print("Result of main.py:\n", result)
        self.assertTrue(len(result) > 0)

    def test_error_bin_cat(self) -> None:
        result = get_file_content("calculator", "/bin/cat")
        # print(result)
        self.assertIn("Error", result)

    def test_not_existing(self) -> None:
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        # print(result)
        self.assertIn("Error", result)
        self.assertIn("pkg/does_not_exist.py", result)

if __name__ == "__main__":
    unittest.main()
