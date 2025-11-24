import os
from google.genai import types
from config import WORKING_DIRECTORY


def write_file(file_path: str, content: str, working_dir: str = WORKING_DIRECTORY) -> str:
    dir_allowed = os.path.abspath(working_dir)
    file_abs_path = os.path.abspath(os.path.join(dir_allowed, file_path))

    if not file_abs_path.startswith(dir_allowed):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(os.path.dirname(file_abs_path)):
            os.makedirs(os.path.dirname(file_abs_path))
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(file_abs_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file within the working directory. Overwrites the file if it already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory where the content should be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    )
)
