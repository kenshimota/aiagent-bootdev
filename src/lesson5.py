import sys
from dotenv import dotenv_values
from google import genai

config = dotenv_values(".env")

api_key: str|None =  config.get("GEMINI_API_KEY") if config.get("GEMINI_API_KEY") is not None else ""
client = genai.Client(api_key=api_key)

class Logger(object):
    def __init__(self) -> None:
        self.is_enabled: bool = False

        for command in sys.argv:
            if command.strip().lower() == "--verbose":
                self.is_enabled = True

    def info(self, message: str) -> None:
        if self.is_enabled:
            print(message)

def main():
    argc: int = len(sys.argv)
    if argc < 2:
        exit(1)

    txt: str = f"{sys.argv[1]}"
    if len(txt) == 0:
        return

    logger = Logger()
    logger.info(f"User prompt: {txt}\n")

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=txt
    )

    meta = res.usage_metadata
    logger.info(f"Prompt tokens: {meta.prompt_token_count}\nResponse tokens: {meta.candidates_token_count}")

    print(f"Response:\n {res.text}")

if __name__ == "__main__":
    main()
