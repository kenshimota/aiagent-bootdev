import os


def write_file(working_dir: str, file_path: str, content: str) -> str:
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
