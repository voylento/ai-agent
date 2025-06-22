import subprocess
from pathlib import Path

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    if file_path == "":
        return f'Error: File "{file_path}" not found.'

    try:
        wp = Path(working_directory).resolve()
        fp = wp.joinpath(file_path).resolve()

        if not str(fp).startswith(str(wp)):
            return (
                f'Error: Cannot execute "{file_path}" as it is '
                "outside the permitted working directory"
            )

        if not fp.exists():
            return f'Error:  File "{file_path}" not found.'

        if fp.suffix != ".py":
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: {e}"

    try:
        commands = ["python3", fp]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=wp,
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Script timed out."
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified python file using subprocess.run and returns the results in a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the python file",
            ),
        },
    ),
)
