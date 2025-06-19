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