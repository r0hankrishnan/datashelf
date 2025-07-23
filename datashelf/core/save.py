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

def _save_pandas_df(df:pd.DataFrame, collection_name:str, name:str, tag:str, message:str) -> bool:
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