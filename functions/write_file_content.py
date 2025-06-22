from pathlib import Path

from google.genai import types


def write_file(working_directory, file_path, content):
    if file_path == "":
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        wp = Path(working_directory).resolve()
        fp = wp.joinpath(file_path).resolve()

        if not str(fp).startswith(str(wp)):
            return (
                f'Error: Cannot read "{file_path}" as it is outside '
                "the permitted working directory"
            )
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(fp, "w") as f:
            res = f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({res} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the file specified with the constraint that the file must be within working_directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file into which to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
