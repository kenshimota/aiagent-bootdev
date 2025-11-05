import sys
from dotenv import dotenv_values
from google import genai

config = dotenv_values(".env")

api_key: str = config.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    argc: int = len(sys.argv)
    if argc < 2:
        exit(1)

    txt: str = f"{sys.argv[1]}"
    if len(txt) == 0:
        return

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=txt
    )
    print(res.text)

    meta = res.usage_metadata
    print(f"Prompt tokens: {meta.prompt_token_count}\nResponse tokens: {
          meta.candidates_token_count}")


if __name__ == "__main__":
    main()
