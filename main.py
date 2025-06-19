import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def print_verbose(user_prompt, response):
    print(f"User prompt: {user_prompt}")
    print()
    print(f"Gemini: {response.text}")
    print()
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def print_concise(response):
    print(f"{response.text}")

def get_args():
    verbose = False

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    if len(sys.argv) > 3:
        print_usage()
        sys.exit(1)

    if len(sys.argv) == 3:
        if sys.argv[2] != "--verbose":
            print(f"Unknown argument: {sys.argv[2]}")
            print_usage()
            exit(1)
        else:
            verbose = True

    user_prompt = sys.argv[1]

    return user_prompt, verbose

def print_usage():
    print("Usage: python3 main.py \"prompt text\" [--verbose]")

def main():
    verbose = False

    user_prompt, verbose = get_args()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages)

    if verbose:
        print_verbose(user_prompt, response)
    else:
        print_concise(response)

if __name__=="__main__":
    main()
