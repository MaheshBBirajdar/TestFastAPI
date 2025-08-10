import os

def validate_file_path(file_path: str, repo_path: str) -> str:
    """
    Validates the file path against the repository structure.
    """
    full_path = os.path.join(repo_path, file_path)

    if file_path.isdigit():
        raise Exception("File path cannot be a number")

    if not file_path or file_path.lower() == 'null':
        raise Exception("File path cannot be empty or null")
    
    if not os.path.exists(full_path):
        raise Exception(f"File '{full_path}' does not exist in the repository")
    
    return file_path


def validate_folder_path(folder_path: str, repo_path: str) -> str:
    """
    Validates the folder path against the repository structure.
    """
    full_path = os.path.join(repo_path, folder_path)

    if not folder_path or folder_path.lower() == 'null':
        raise Exception("Folder path cannot be empty or null")
    
    if not os.path.exists(full_path):
        raise Exception(f"Folder '{full_path}' does not exist in the repository")
    
    return folder_path