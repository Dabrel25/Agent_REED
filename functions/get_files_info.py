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
    