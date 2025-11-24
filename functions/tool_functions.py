from google.genai import types
from typing import Dict

from functions.logger import Logger
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


def procedure_fn(function_call_part):
    logger = Logger()

    logger.debug(f"Calling function: {
                 function_call_part.name}({function_call_part.args})")
    logger.only_production(f"Calling function: {function_call_part.name}")

    functions: Dict[str, any] = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if not functions.get(function_call_part.name):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {
                        function_call_part.name}"},
                )
            ],
        )

    args = dict(function_call_part.args)
    res = functions[function_call_part.name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": res},
            )
        ]
    )


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
