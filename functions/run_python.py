import os
import subprocess
from typing import List
from google.genai import types
from config import WORKING_DIRECTORY


def run_python_file(file_path: str, working_dir: str = WORKING_DIRECTORY, args: List[str] = []) -> str:
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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file located within the working directory and return its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory of the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python file when executing it.",
            )
        }
    )
)
