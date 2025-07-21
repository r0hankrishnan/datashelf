import os
import pathlib
from pathlib import Path

def _find_datashelf_root(return_datashelf_path:bool = False) -> pathlib.PosixPath:

    """This funciton walks up the file tree, starting in the directory from which it was called, 
    until it finds the directory that is the direct parent of the .datashelf folder

    Returns:
        pathlib.PosixPath: path of directory containing the .datashelf folder (called root directory for our purposes)
    """
    
    # Set starting point as the working directory of whatever file the user is working in 
    current = Path.cwd()
    
    # Walk up file tree to find directory where .datashelf is and treat that as root
    while current != current.parent:
        if (current/'.datashelf').exists():
            return current/'.datashelf' if return_datashelf_path else current
        else:
            current = current.parent
    
    # If while loop terminates, that means the function went through all directories in that path and didn't find .datashelf
    return None


def _get_collection_files(collection_name:str):
    import yaml
    collection_path = os.path.join(_find_datashelf_root(return_datashelf_path= True), collection_name.lower().replace(" ", "_"))
    collection_metadata_path = os.path.join(collection_path, f'{collection_name.lower().replace(" ", "_")}_metadata.yaml')
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return data['files']