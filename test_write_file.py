import unittest
from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_write_lorem(self) -> None:
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        # print("Result for lorem.txt")
        # print(result)
        self.assertIn("Successfully wrote to", result)
        self.assertIn("lorem.txt", result)
        self.assertIn("28 characters written", result)


    def test_write_morelorem(self) -> None:
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        # print("Result for morelorem.txt")
        # print(result)
        self.assertIn("Successfully wrote to", result)
        self.assertIn("morelorem.txt", result)
        self.assertIn("26 characters written", result)

    def test_write_temp(self) -> None:
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        # print("Result for temp.txt")
        # print(result)
        self.assertIn("Error", result)



if __name__ == "__main__":
    unittest.main()
