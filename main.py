from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-flash-lite"

system_prompt = """
You are an experienced senior software engineer and programming mentor.
Explain technical concepts clearly and use simple examples when appropriate.
Adapt your explanations to the user's programming level.
Remember previous messages and maintain the conversation context.
"""

chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=1000,
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    )
)

conversation_history = []

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    if user_input.lower() == "history":
        if not conversation_history:
            print("The conversation is empty.")
        else:
            for message in conversation_history:
                print(message["role"].upper() + ":")
                print(message["content"])
        continue

    if not user_input:
        continue

    try:
        response = chat.send_message(user_input)
        assistant_message = response.text

        conversation_history.append({
            "role": "user",
            "content": user_input
        })

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        print("AI:", assistant_message)

    except Exception as error:
        print("Error:", error)
