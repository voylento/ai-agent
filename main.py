import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_file_content import schema_write_file
from prompts import system_prompt

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def print_usage():
    print('Usage: python3 main.py "prompt text" [--verbose]')


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print_usage()
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")

    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]  # noqa: E501

    client = genai.Client(api_key=api_key)

    iteration_count = 10

    try:
        while iteration_count > 0:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            if not response.function_calls:
                print(f"{response.text}")
                return response.text

            for func_call in response.function_calls:
                func_response = call_function(func_call)
                messages.append(func_response)
                if (
                    not func_response.parts
                    or not func_response.parts[0].function_response.response
                ):
                    raise Exception(
                        f"function response does not contain valid parts: {
                            func_response
                        }"
                    )

                if verbose:
                    print(f"-> {func_response.parts[0].function_response.response}")

            iteration_count -= 1
    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()
