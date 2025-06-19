from pathlib import Path

def is_directory_allowed(working_dir, directory=None):
    """
    Check if directory is the working directory or a subdirectory of it.
    Returns True if allowed, False if not allowed.
    """
    working_path = Path(working_dir).resolve()
    user_path = Path(directory).resolve()
    
    # First check if the user path actually exists
    if not user_path.exists():
        return False
    
    # Check if working_path is the same as user_path OR is a parent of user_path
    return working_path == user_path or working_path in user_path.parents


def get_files_info(working_directory, directory=None):
    if not is_directory_allowed(working_directory, directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    user_path = Path(directory)
    if not user_path.is_dir():
        return f'Error: "{directory}" is not a directory'

    strings = [] 

    files = [entry for entry in user_path.iterdir()]
    
    try:
        for entry in files:
            file_info = f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}"
            strings.append(file_info)
    except Exception as e:
        strings.append(f"Error: {e}")

    return "\n".join(strings)


