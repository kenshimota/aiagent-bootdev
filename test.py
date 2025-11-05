from google import genai
from dotenv import dotenv_values
from google.genai import types

config = dotenv_values(".env")

api_key: str = config.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    messages = []

    while True:
        msg: str = input("Escribe tu pregunta (escribe 'exit' para salir): ")
        msg = msg.strip()

        if msg.strip().lower() == 'exit':
            break

        messages.append(types.Content(
            role="user", parts=[types.Part(text=msg)]))

        res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages
        )

        messages.append(types.Content(role="model", parts=[
                        types.Part(text=res.text)]))
        print(f"Machine Ai: {res.text}\n")

        meta = res.usage_metadata
        print(f"Prompt tokens: {meta.prompt_token_count}\nResponse tokens: {
              meta.candidates_token_count}")

    print("¡Hasta luego! fue un placer ayudarte.")


if __name__ == "__main__":
    main()
