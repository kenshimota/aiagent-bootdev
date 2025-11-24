import sys
from google import genai
from google.genai import types
from dotenv import dotenv_values
from functions.tool_functions import available_functions, procedure_fn
from functions.logger import Logger

config = dotenv_values(".env")

api_key: str | None = config.get("GEMINI_API_KEY") if config.get(
    "GEMINI_API_KEY") is not None else ""
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
- Read file contents
Read files only within the working directory.
- Execute Python files with optional arguments
Execute only Python files within the working directory. and provide any necessary arguments.
- Write or overwrite files
Write files only within the working directory. each time you write to a file, you overwrite its previous contents.
"""


def main():
    argc: int = len(sys.argv)
    if argc < 2:
        exit(1)

    txt: str = f"{sys.argv[1]}"
    if len(txt) == 0:
        return

    logger = Logger()
    logger.debug(f"User prompt: {txt}\n")

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=txt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions])
    )

    meta = res.usage_metadata
    logger.debug(f"Prompt tokens: {meta.prompt_token_count}\nResponse tokens: {
        meta.candidates_token_count}")

    for function_call_part in res.function_calls:
        procedure_response = procedure_fn(function_call_part)
        res = procedure_response.parts[0].function_response
        logger.debug(f"-> {res}")


if __name__ == "__main__":
    main()
