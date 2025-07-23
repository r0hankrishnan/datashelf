import os
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.shelf import _update_datashelf_metadata_with_added_collection
from datashelf.utils.logging import setup_logger
import pandas as pd

logger = setup_logger(__name__)

def create_collection(collection_name:str):
    """
    First checks if .datashelf exists anywhere between the current working directory and the filesystem root.
    Then, finds the .datashelf path and checks if the collection folder and metadata filee already exist.
    If they don't exist, it creates the collection folder inside the .datashelf directory. 
    If the collection exists but the metadata file does not, it creates the metadata file in the collection folder 
    (this should also probably raise some type of error).

    Args:
        collection_name (str): The name of the collection you want to create. All strings will be lowercased and have 
        their spaces replaced with underscores.

    Raises:
        NotADirectoryError: If the function cannot find a .datashelf directory in the file tree, it will raise an error 
        and prompt you to initialize a new datashelf before trying to create a collection.
    """
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    
    # Check that datashelf has been initialized
    if os.path.isdir(datashelf_path):
        pass
    else:
        raise NotADirectoryError(".datashelf does not exist. Please initialize datashelf with init() before creating a collection.")

    collection_path = os.path.join(datashelf_path, collection_name.lower().replace(" ", "_"))
    metadata_filename = collection_name.lower().replace(" ", "_") + "_metadata.yaml"
    
    # Make collection subfolder in .datashelf
    if os.path.isdir(collection_path):
        _create_only_collection_metadata(collection_name = collection_name, collection_path = collection_path, metadata_filename = metadata_filename)
        
    else:
        _create_collection_dir_and_metadata(collection_name = collection_name, collection_path = collection_path, metadata_filename = metadata_filename)

def _create_only_collection_metadata(collection_name:str, collection_path:str, metadata_filename:str) -> bool:
    
    if os.path.exists(os.path.join(collection_path, metadata_filename)):
        logger.info(f"Collection already exists at {collection_path} with metadata file: {metadata_filename}.")
        return 1
    else:
        logger.info(f"collection directory: {collection_name} exists but does not have a metadatafile.\nCreating {metadata_filename}...")
        try:
            with open(os.path.join(collection_path, metadata_filename), 'w') as f:
                pass
            _make_collection_metadata_structure(collection_name = collection_name)
            _update_datashelf_metadata_with_added_collection(collection_name = collection_name)
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        
        logger.info(f"Metadata file: {metadata_filename} created in {collection_path}.")
        return 0
    
def _create_collection_dir_and_metadata(collection_name:str, collection_path:str, metadata_filename:str) -> bool:
    os.makedirs(collection_path, exist_ok = True)
    try:
        with open(os.path.join(collection_path, metadata_filename), 'w') as f:
            pass
        _make_collection_metadata_structure(collection_name = collection_name)
        _update_datashelf_metadata_with_added_collection(collection_name = collection_name)
        
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    
    logger.info(f"Collection directory: {collection_name} and metadatafile: {metadata_filename} created.")
    return 0