import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

schema_get_files_info = type.FunctionDeclaration (
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory."
    parameters=types.Schema (
        type=type.Type.OBJECT,
        properties={
            "directory": types.Schema (
                type=types.Type.STRING,
                description="The directory from which to list the files, relative to the working directory. If not provided, lists files in the working directory.",
            )
        }
    )
)

schema_get_file_content = type.FunctionDeclaration (
    name="get_file_content",
    description="Lists the content of a file given a file path and a working directory, constrained to be in the working directory or in a child directory of the working directory."
    parameters.types.Schema (
        type-type.Type.OBJECT,
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


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
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if verbose:
        print_verbose(user_prompt, response)
    else:
        print_concise(response)

if __name__=="__main__":
    main()
