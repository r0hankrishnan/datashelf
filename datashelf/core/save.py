import pandas as pd
from datashelf.utils.tools import _find_datashelf_root, _get_collection_files
from datashelf.core.metadata import _get_next_version_number, _add_file_to_collection_metadata,\
    _update_collection_metadata_info, _update_datashelf_metadata_collection_files
from datashelf.utils.hashing import _hash_pandas_df
from datashelf.utils.logging import setup_logger
from datashelf.core.config import check_tag_enforcement, get_allowed_tags

logger = setup_logger(__name__)
   
def save(df:pd.DataFrame, collection_name:str, name:str, tag:str, message:str):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        collection_name (str): _description_
        name (str): _description_
        tag (str): _description_
        message (str): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    
    # Tag checking
    tags_enforced = check_tag_enforcement()
    allowed_tags = get_allowed_tags()
    
    if tags_enforced:
        if tag in allowed_tags:
            pass
        else:
            err_msg = (f'{tag} is not a valid tag.'
                       f'Tag enforcement is currently set to {tags_enforced}.'
                       f'You cannot change enforcement as of this version of DataShelf.'
                       f'Please use one of the following allowed tags {", ".join(allowed_tags)}')
            logger.error(err_msg)
            raise ValueError(err_msg)
    
    # Run pandas process if passed a pandas df
    if isinstance(df, pd.DataFrame):
        _pandas_save_df(df, collection_name, name, tag, message)
        return 0
    
    # Return err msg for polars
    elif isinstance(df, pl.DataFrame):
        err_msg = "Polars not currently supported, sorry!"
        logger.error(err_msg)
        raise ValueError(err_msg)
    
    # Return err for all other types
    else:
        err_msg = "Unsupported data type. DataShelf only supports pandas DataFrames at the moment."
        logger.error(err_msg)
        raise ValueError(err_msg)

def _pandas_save_df(df:pd.DataFrame, collection_name:str, name:str, tag:str, message:str):
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        collection_name (str): _description_
        name (str): _description_
        tag (str): _description_
        message (str): _description_

    Raises:
        an: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    hashed_df = _hash_pandas_df(df)
    collection_files = _get_collection_files(collection_name = collection_name)
    file_name = f'{name.lower().replace(" ", "_")}_{tag}'
    collection_path = _find_datashelf_root(return_datashelf_path=True)/collection_name.lower().replace(" ", "_")
    file_path_base = collection_path/file_name
    
    version_number = _get_next_version_number(collection_name = collection_name, collection_path = collection_path)    
    
    if version_number == 1: 
        file_type = _pandas_assign_smart_save(df = df)
        file_path = str(file_path_base) + file_type
        
        _save_and_register_df(df = df, file_type = file_type, collection_name = collection_name, file_name = name,
                              tag = tag, message = message, df_hash = hashed_df, version = version_number,
                              file_path = file_path, collection_path = collection_path)
            
        logger.info(f"{name} added to {collection_name}")
        return 0
        
    elif len(collection_files) > 1:
        for _, file in enumerate(collection_files):
            if file['hash'] == hashed_df:
                logger.info(f"{name}'s hash matches a dataframe that is already saved in datashelf: {file['name']}.")
                return 1
            else:
                pass
        
        file_type = _pandas_assign_smart_save(df = df)
        file_path = str(file_path_base) + file_type

        _save_and_register_df(df = df, file_type = file_type, collection_name = collection_name, file_name = name,
                              tag = tag, message = message, df_hash = hashed_df, version = version_number,
                              file_path = file_path, collection_path = collection_path)

        logger.info(f"{name} added to {collection_name}")
        return 0
        
    
    else:
        err_msg = (
            f"There are 0 files in {collection_name}'s metadata file. "
            "Something went wrong with it's initialization. "
            "Please try recreating the collection or raise an issue on GitHub!"
        )
        logger.error(err_msg)
        raise ValueError(err_msg)
                 
def _pandas_assign_smart_save(df:pd.DataFrame):
    """_summary_

    Args:
        df (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    df_size = df.memory_usage(deep = True).sum()
    
    threshold = 10 * 1024 * 1024 # 10MB
    
    if df_size < threshold:
        logger.info(f'Save as CSV ({df_size / 1e6:.2f} MB)')
        return '.csv'
    else:
        logger.info(f'Save as Parquet ({df_size / 1e6:.2f} MB)')
        return '.parquet'
    
def _save_and_register_df(df, file_type:str, collection_name:str, file_name:str, tag:str, message:str, df_hash:str, 
                          version:int, file_path:str, collection_path:str):
    """_summary_

    Args:
        df (_type_): _description_
        file_type (str): _description_
        collection_name (str): _description_
        file_name (str): _description_
        tag (str): _description_
        message (str): _description_
        df_hash (str): _description_
        version (int): _description_
        file_path (str): _description_
        collection_path (str): _description_

    Returns:
        _type_: _description_
    """
    
    if file_type == '.csv':
        df.to_csv(file_path, index = False)
        _add_file_to_collection_metadata(collection_name = collection_name, file_name = file_name, tag = tag, 
                                            message = message, df_hash = df_hash, version = version, 
                                            file_path = file_path)
        _update_collection_metadata_info(collection_name = collection_name, saved_df_file_path = file_path, new_version = version)
        _update_datashelf_metadata_collection_files(collection_name = collection_name, collection_path = collection_path)

        return 0
        
    else:
        df.to_parquet(file_path, index = False)
        _add_file_to_collection_metadata(collection_name = collection_name, file_name = file_name, tag = tag, 
                                            message = message, df_hash = df_hash, version = version, 
                                            file_path = file_path)
        _update_collection_metadata_info(collection_name = collection_name, saved_df_file_path = file_path, new_version = version)
        _update_datashelf_metadata_collection_files(collection_name = collection_name, collection_path = collection_path)
        
        return 0
            