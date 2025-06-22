from pathlib import Path

from google.genai import types


def get_files_info(working_directory, directory=None):
    dir_path = None

    if directory is None:
        dir_path = Path(working_directory).resolve()
    else:
        working_path = Path(working_directory).resolve()
        dir_path = working_path.joinpath(directory).resolve()

        if not str(dir_path).startswith(str(working_path)):
            return (
                f'Error: Cannot list "{directory}" as it is outside '
                "the permitted working directory"
            )

        if not dir_path.exists():
            return f'Error: "{directory} is not a directory'

        if not dir_path.is_dir():
            return f'Error: "{directory}" is not a directory'

    strings = []

    files = [entry for entry in dir_path.iterdir()]

    try:
        for entry in files:
            file_info = f"- {entry.name}: file_size={
                entry.stat().st_size
            } bytes, is_dir={entry.is_dir()}"
            strings.append(file_info)
    except Exception as e:
        strings.append(f"Error: {e}")

    return "\n".join(strings)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory from which to list the files, relative to the working directory. If not provided, lists files in the working directory.",
            ),
        },
    ),
)
