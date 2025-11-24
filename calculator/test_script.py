
# test_script.py
import subprocess

test_cases = [
    ("10", "5", "+"),
    ("10", "5", "-"),
    ("10", "5", "*"),
    ("10", "5", "/"),
    ("7", "3", "+"),
    ("7", "3", "-"),
    ("7", "3", "*"),
    ("7", "3", "/"),
]

for num1, num2, operator in test_cases:
    print(f"Testing with: {num1} {operator} {num2}")
    result = subprocess.run(["python", "main.py", num1, num2, operator], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
