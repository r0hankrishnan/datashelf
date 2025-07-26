from pathlib import Path
import pathlib
from typing import Union
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.logging import setup_logger
from datashelf.core.metadata import _initialize_collection_metadata, _add_collection_to_datashelf_metadata

logger = setup_logger(__name__)

def create_collection(collection_name:str):
    """ Checks if .datashelf exists and if collection directory already exists and is not corrupted. If all checks pass, 
    creates the collection folder inside the .datashelf directory, initializes a {collection_name}_metadata.yaml file,
    and updates the datashelf_metadata.yaml file with the newly created collection's information.

    Args:
        collection_name (str): The name of the collection being created. 
        Will automatically be converted into snake case. Avoid using any characters other than spaces and underscores.

    Raises:
        NotADirectoryError: Raised if function cannot find your .datashelf directory
        FileNotFoundError: Raised if function finds existing collection directory without a metadata file. This is a sign
        that the process is corrupted and the user should consider deleting the entire .datashelf directory and re-initialize.
    """
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    
    # Check that datashelf has been initialized
    if datashelf_path is None or not datashelf_path.is_dir():
        raise NotADirectoryError(".datashelf does not exist. Please initialize datashelf with init() before creating a collection.")
    else:
        pass

    collection_path = datashelf_path/collection_name.lower().replace(" ", "_")
    metadata_filename = collection_name.lower().replace(" ", "_") + "_metadata.yaml"
    
    # Check for potential collection file corruption
    if collection_path.exists():
        collection_metadata_path = datashelf_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'

        if collection_metadata_path.exists():
            logger.info(f"Collection '{collection_name}' already exists with metadata.")
            return
        else:
            raise FileNotFoundError(
                f"Collection directory '{collection_path}' exists but the metadata file '{metadata_filename}' does not.\n"
                f"This may indicate a corrupted or manually modified state. Consider deleting and recreating the collection."
            )
            
    # If all checks pass, create collection, initialize collection metadata, and update datashelf metadata
    else:
        _create_collection(collection_path = collection_path, collection_name = collection_name)
        return 0
    
    
    
def _create_collection(collection_path:Union[str,pathlib.PosixPath], collection_name:str):
    """Creates a folder with a snake-cased collection_name at collection_path. Then, initializes the collection's
    metadata and updates the datashelf_metadata.yaml file to reflect the newly added collection.

    Args:
        collection_path (Union[str,pathlib.PosixPath]): The directory path of the collection folder (pulled from create_collection).
        collection_name (str): The name of the collection to be created (pulled from create_collection).

    Returns:
        _type_: Returns a 0 if all operations pass successfully. 
    """
    # Create collection folder
    collection_path = Path(collection_path)
    collection_path.mkdir(parents = True, exist_ok = True)
    
    # Create default collection metadata file
    _initialize_collection_metadata(collection_name = collection_name)
    
    #Update datashelf metadata with new collection
    _add_collection_to_datashelf_metadata(collection_name = collection_name)
    
    logger.info(f'Collection directory: {collection_name.lower().replace(" ", "_")} and metadata file created.')
    return 0