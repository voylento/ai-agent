from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file_content import write_file

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

working_directory = "calculator"


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f" - Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name in function_map:
        function_result = function_map[function_name](working_directory, **args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
