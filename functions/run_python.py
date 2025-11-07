import os
import subprocess
from typing import List


def run_python_file(working_dir: str, file_path: str, args: List[str] = []) -> str:
    dir_allowed = os.path.abspath(working_dir)
    file_abs_path = os.path.abspath(os.path.join(dir_allowed, file_path))

    if not file_abs_path.startswith(dir_allowed):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_abs_path):
        return f'Error: File "{file_path}" not found.'

    if not file_abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    command: List[str] = ["python", file_abs_path] + args

    try:
        res = subprocess.run(command, capture_output=True,
                             text=True, timeout=30, cwd=dir_allowed)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = []
    if res.stdout:
        output.append(f"STDOUT:\n{res.stdout}")
    if res.stderr:
        output.append(f"STDERR:\n{res.stderr}")
    if res.returncode != 0:
        output.append(f"Process exited with code {res.returncode}")

    return "\n".join(output) if len(output) > 0 else "Not output produced."
