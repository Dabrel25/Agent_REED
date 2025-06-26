import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."

    complete_path = os.path.join(working_directory, directory)
    abs_complete_path = os.path.abspath(complete_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_complete_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_complete_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        list_items = os.listdir(abs_complete_path)
        list_of_strings = []
        for item in list_items:
            item_path = os.path.join(abs_complete_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            list_of_strings.append(f'- {item}: file_size={file_size} bytes, is_dir={is_dir}')
        
        return "\n".join(list_of_strings)
    except Exception as e:
        return f'Error: {str(e)}'

def get_file_content(working_directory, file_path):

    complete_file_path = os.path.join(working_directory, file_path)
    abs_complete_file_path = os.path.abspath(complete_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_complete_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_complete_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_complete_file_path, 'r') as file:
            file_content_string = file.read(10000)
            if len(file.read(1)) == 0:
                return file_content_string
            return f'{file_content_string} \n ...File "{file_path}" truncated at 10000 characters'
    except Exception as e:
        return f'Error: {str(e)}'

def write_file(working_directory, file_path, content):
    complete_file_path = os.path.join(working_directory, file_path)
    abs_complete_file_path = os.path.abspath(complete_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_complete_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.dirname(abs_complete_file_path)):
        return f'Error: Cannot write to "{file_path}" as the parent directory does not exist'

    try:
        with open(abs_complete_file_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'



def run_python_file(working_directory, file_path):
    complete_file_path = os.path.join(working_directory, file_path)
    abs_complete_file_path = os.path.abspath(complete_file_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_complete_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_complete_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_complete_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", abs_complete_file_path ],  # Command as a list
            cwd= abs_working_dir,  # Set working directory
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Return strings instead of bytes
            timeout=30  # Timeout in seconds
        )
        # output content
        stdout_content = result.stdout
        stderr_content = result.stderr
        exit_code = result.returncode

        # If there's stdout content
        output_parts = []

        # Add stdout if it exists
        if stdout_content:
            output_parts.append(f"STDOUT: {stdout_content}")

        # Add stderr if it exists
        if stderr_content:
            output_parts.append(f"STDERR: {stderr_content}")

        # Add exit code if non-zero
        if exit_code != 0:
            output_parts.append(f"Process exited with code {exit_code}")

        # If no output at all
        if not output_parts:
            return "No output produced."

        # Join all parts and return
        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
