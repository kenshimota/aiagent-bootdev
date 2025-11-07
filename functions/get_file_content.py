import os
from config import LIMIT_TO_READ_FROM_FILE

# maximum number of characters to read from the file
limit = LIMIT_TO_READ_FROM_FILE


def get_file_content(working_directory, file_path):
    root_path = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_path.startswith(root_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path, "r", encoding="utf-8") as file:
            string_content = file.read(LIMIT_TO_READ_FROM_FILE + 1)
            if len(string_content) == limit + 1:
                string_content += f'[...File "{
                    file_path}" truncated at {limit} characters]'

    except Exception as e:
        return f'Error: {e}'

    return string_content
