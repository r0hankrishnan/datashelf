import os
from datashelf.utils.tools import _find_datashelf_root, _get_collection_files
from datashelf.utils.shelf import _make_datashelf_metadata_structure, \
    _update_datashelf_metadata_with_added_collection, _update_datashelf_metadata_with_added_file_in_collection
from datashelf.utils.collection import _make_collection_metadata_structure, \
    _add_file_to_collection_metadata, _update_config_metadata
from datashelf.utils.hashing import _hash_pandas_df
from datashelf.utils.logging import setup_logger
import pandas as pd

logger = setup_logger(__name__)

def init(set_dir:str = None):
    """_summary_

    Args:
        set_dir (str, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    
    ## These top level if statements should probably be turned into helper functions for readibility
    
    # If user sets a specific path for .datashelf
    if set_dir:
        _init_with_set_dir(set_dir = set_dir)
    
    # If no set path, initialize .datashelf in cwd
    else:
        _init_with_current_dir()
        
def _init_with_set_dir(set_dir:str):
        
    # Make sure user isn't trying to create .datashelf in a subdirectory of current dir
    current_dir = os.path.abspath(os.getcwd())
    target_dir = os.path.abspath(set_dir)
    
    # Check if target_dir is a subdirectory of current_dir
    if target_dir.startswith(current_dir + os.sep):
        raise ValueError(
            f"Cannot initialize datashelf in a subdirectory ({target_dir}). "
            f"Datashelf should be initialized at or above the current directory "
            f"to ensure it can be found from all project files. "
            f"Consider running init() without set_dir, or use a parent directory."
        )
        
    elif os.path.isdir(os.path.join(set_dir, '.datashelf')) and os.path.exists(os.path.join(set_dir, '.datashelf', 'datashelf_metadata.yaml')):
        return logger.info(".datashelf directory and metadata already initalized.")
    else:
        os.makedirs(os.path.join(set_dir, '.datashelf'), exist_ok = True)
    
    # Should define and add in basic config data to YAML here
        try:
            _make_datashelf_metadata_structure()
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
    
        return logger.info(".datashelf directory and metadata initialized")
        
    
    
def _init_with_current_dir():

    # Warning message about running init() in the right directory
    while True:
        cont = input("It is recommended that you init datashelf in your project's root directory.\nPlease check that you are in the correct directory before continuing.\nContinue (y/n)?")
        if cont.lower().strip() in ["yes", "y"]:
            break
        elif cont.lower().strip() in ["no", "n"]:
            return None

    # Check current directory for .datashelf and create if DNE
    if os.path.isdir('.datashelf') and os.path.exists(os.path.join(os.getcwd(), '.datashelf', 'datashelf_metadata.yaml')):
        return logger.info(".datashelf directory and metadata already initalized.")
    else:
        os.makedirs('.datashelf', exist_ok = True)
        
        # Should define and add in basic config data to YAML here
        try:
            _make_datashelf_metadata_structure()
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        
        return logger.info(".datashelf directory and metadata initialized")