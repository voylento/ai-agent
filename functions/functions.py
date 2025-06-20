from pathlib import Path
import subprocess

def validate_directory_path(working_directory, directory=None):
    dir_path = None

    if directory == None:
        dir_path = Path(working_directory).resolve()
    else:
        working_path = Path(working_directory).resolve()
        dir_path = working_path.joinpath(directory).resolve()

        if not str(dir_path).startswith(str(working_path)):
            return False, f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not dir_path.exists():
            return False, f'Error: "{directory} is not a directory'

        if not dir_path.is_dir():
            return False, f'Error: "{directory}" is not a directory'

    return True, ""

def get_files_info(working_directory, directory=None):
    dir_path = None

    if directory == None:
        dir_path = Path(working_directory).resolve()
    else:
        working_path = Path(working_directory).resolve()
        dir_path = working_path.joinpath(directory).resolve()

        if not str(dir_path).startswith(str(working_path)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not dir_path.exists():
            return f'Error: "{directory} is not a directory'

        if not dir_path.is_dir():
            return f'Error: "{directory}" is not a directory'


    strings = [] 

    files = [entry for entry in dir_path.iterdir()]
    
    try:
        for entry in files:
            file_info = f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}"
            strings.append(file_info)
    except Exception as e:
        strings.append(f"Error: {e}")

    return "\n".join(strings)


def get_file_content(working_directory, file_path):
    file_content_string = ""

    if file_path == "":
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        wp = Path(working_directory).resolve()
        fp = wp.joinpath(file_path).resolve()

        if not str(fp).startswith(str(wp)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not fp.exists() or not fp.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'

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

def write_file(working_directory, file_path, content):
    if file_path == "":
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        wp = Path(working_directory).resolve()
        fp = wp.joinpath(file_path).resolve()

        if not str(fp).startswith(str(wp)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(fp, "w") as f:
            res = f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({res} characters written)'

def run_python_file(working_directory, file_path):
    if file_path == "":
        return f'Error: File "{file_path}" not found.'

    try:
        wp = Path(working_directory).resolve()
        fp = wp.joinpath(file_path).resolve()

        if not str(fp).startswith(str(wp)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

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
        return "Error: executing Python file: Script timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"

