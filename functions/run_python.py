import os
import subprocess


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