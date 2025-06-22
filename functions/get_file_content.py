from pathlib import Path

from google.genai import types


def get_file_content(working_directory, file_path):
    file_content_string = ""

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

        if not fp.exists() or not fp.is_file():
            return 'Error: File not found or is not a regular file: "{file_path}"'  # noqa: E501

    except Exception as e:
        return f"Error: {e}"

    try:
        with open(fp, "r") as f:
            file_content_string = f.read(10001)
    except Exception as e:
        return f"Error: error reading file {e}"

    if len(file_content_string) > 10000:
        file_content_string = file_content_string[:9999]
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file constrained to the working directory. Content truncated at 10000 words.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file from which to read content.",
            ),
        },
    ),
)
