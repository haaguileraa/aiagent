from functions.run_python_file import run_python_file

def run_calculator_main_no_args() -> None:
    result = run_python_file("calculator", "main.py")
    print("Result for calculator/main.py without args")
    print(result)

def run_calculator_main_args() -> None:
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for caltulator/main.py with args")
    print(result)

def run_calculator_tests() -> None:
    result = run_python_file("calculator", "tests.py")
    print("Result for tests")
    print(result)

def error_calculator_main() -> None:
    result = run_python_file("calculator", "../main.py")
    print("Result for main out of working dir")
    print(result)

def error_non_existent() -> None:
    result = run_python_file("calculator", "nonexistent.py")
    print("Result for nonexistent:")
    print(result)

def error_non_python() -> None:
    result = run_python_file("calculator", "lorem.txt")
    print("Result for lorem.txt:")
    print(result)

if __name__ == "__main__":
    run_calculator_main_no_args()
    run_calculator_main_args()
    run_calculator_tests()
    error_calculator_main()
    error_non_existent()
    error_non_python()
