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
       

def create_collection(collection_name:str):
    """
    First checks if .datashelf exists anywhere between the current working directory and the filesystem root.
    Then, finds the .datashelf path and checks if the collection folder and metadata filee already exist.
    If they don't exist, it creates the collection folder inside the .datashelf directory. 
    If the collection exists but the metadata file does not, it creates the metadata file in the collection folder 
    (this should also probably raise some type of error).

    Args:
        collection_name (str): The name of the collection you want to create. All strings will be lowercased and have their spaces replaced with underscores.

    Raises:
        NotADirectoryError: If the function cannot find a .datashelf directory in the file tree, it will raise an error and prompt you to initialize a new datashelf before trying to create a collection.
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
        if os.path.exists(os.path.join(collection_path, metadata_filename)):
            return logger.info(f"collection already exists at {collection_path} with metadata file: {metadata_filename}.")
        else:
            logger.info(f"collection directory: {collection_name} exists but does not have a metadata file.\nCreating {metadata_filename}...")
            try:
                with open(os.path.join(collection_path, metadata_filename), 'w') as f:
                    pass
                _make_collection_metadata_structure(collection_name = collection_name)
                _update_datashelf_metadata_with_added_collection(collection_name = collection_name)
                
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise
            return logger.info(f"Metadata file: {metadata_filename} created in {collection_path}.")
        
    else:
        os.makedirs(collection_path, exist_ok = True)
        try:
            with open(os.path.join(collection_path, metadata_filename), 'w') as f:
                pass
            _make_collection_metadata_structure(collection_name = collection_name)
            _update_datashelf_metadata_with_added_collection(collection_name = collection_name)
            
        except Exception as e:
            logger.error(f"An error occured: {e}")
            raise
        
        #UPDATE DATASHELF METADATA HERE
        return logger.info(f"collection directory: {collection_name} and metadata file {metadata_filename} created.")

def _create_only_collection_metadata():
    ...

def _create_collection_dir_and_metadata():
    ...


def save(df:pd.DataFrame, collection_name:str, name:str, tag:str, message:str):
    """Take in a pd.DataFrame, save it as a pickle or csv (not sure which yet, maybe based on size) and 
    store file name + metadata in log file and update last_modified field in overall metadata

    Args:
        df (pd.DataFrame): _description_
        collection (str): _description_
        message (str): _description_
    """
    # This should probably get extracted into some helper functions at some point
    if isinstance(df, pd.DataFrame):
        
        hashed_df = _hash_pandas_df(df)
        
        collection_files = _get_collection_files(collection_name = collection_name)
        
        file_name = f'{name.lower().replace(" ", "_")}_{tag}.csv'
        
        collection_path = _find_datashelf_root(return_datashelf_path=True)/collection_name.lower().replace(" ", "_")
        
        file_path = os.path.join(collection_path, file_name)
        
                
        if len(collection_files) == 1:
            # Could rework this function to directly take in the data that is loaded in _get_collection_files
            # that way, we don't have to open the metadata file twice to get the same info.
            _add_file_to_collection_metadata(collection_name = collection_name, file_name = name, tag = tag, message = message, 
                                         file_hash = hashed_df)
            
            df.to_csv(file_path)
            
            _update_config_metadata(collection_name = collection_name, most_recent_commit = file_path)
            _update_datashelf_metadata_with_added_file_in_collection(collection_name = collection_name, collection_path = collection_path)
            
            return logger.info(f"{name} added to {collection_name}")
            
        elif len(collection_files) > 1:
            for i, file in enumerate(collection_files):
                if file['hash'] == hashed_df:
                    return logger.info(f"{name}'s hash matches a dataframe that is already saved in datashelf: {file['name']}.")
                else:
                    pass
                
            _add_file_to_collection_metadata(collection_name = collection_name, file_name = name, tag = tag, message = message, 
                                         file_hash = hashed_df)
            
            df.to_csv(file_path)
            
            _update_config_metadata(collection_name = collection_name, most_recent_commit = file_path)
            _update_datashelf_metadata_with_added_file_in_collection(collection_name = collection_name, collection_path = collection_path)

            return logger.info(f"{name} added to {collection_name}")
            
        
        else:
            logger.info(f"There are 0 files in {collection_name}'s metadata file. Something went wrong with it's initialization. Please try recreating the collection or raise an issue on GitHub!")
            raise
              
    # Evenutally add polars support
    elif isinstance(df, pl.DataFrame):
        return logger.error("DataShelf does not current support polars DataFrames, sorry!")
        
    else:
        return logger.error("Data is not a recognized DataFrame. DataShelf only supports pandas DataFrames for now.")
    
def ls():
    # List datashelf's metadata file
    ...

def display_collection():
    # Display pretty table of collection's metadata
    ...
    
def load():
    # Load in a particular file from .datashelf folder by name
    ...

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