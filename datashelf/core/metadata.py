import yaml
import pathlib
from pathlib import Path
from typing import Union, Literal
from datetime import datetime
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.logging import setup_logger
from datashelf.utils.tools import _get_collection_files

logger = setup_logger(__name__)

################################################################################
# Top-level datashelf meatadata helpers
################################################################################

# Initialize datashelf metadata file
def _initialize_datashelf_metadata(set_dir:str = None):
    """_summary_

    Args:
        set_dir (str, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    
    # Manually set path if set_dir is not None
    if set_dir:
        datashelf_path = Path(set_dir).resolve()/'.datashelf'
        datashelf_metadata_path = datashelf_path/'datashelf_metadata.yaml'
    else:
        datashelf_path = _find_datashelf_root(return_datashelf_path = True)
        datashelf_metadata_path = datashelf_path/'datashelf_metadata.yaml'
        
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Only add directories since collections are initialized as directories
    collections = [collection for collection in datashelf_path.iterdir() if collection.is_dir()]
    num_collections = len(collections)
    
    metadata = {}
    metadata['metadata'] = {'date_created': current_timestamp,
                            'number_of_collections': num_collections,
                            'collections': collections}
    metadata['collections'] = []
    
    with open(datashelf_metadata_path, 'w') as f:
        yaml.safe_dump(metadata, f, sort_keys = False)
        
    return 0

# Add a collection to metadata - Used inside create_collection()
def _add_collection_to_datashelf_metadata(collection_name:str):
    # Get path variables
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    datashelf_metadata_path = datashelf_path/'datashelf_metadata.yaml'
    collection_path = datashelf_path/f'{collection_name.lower().replace(" ", "_")}'
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read current datashelf_metadata.yaml
    with open(datashelf_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Update metadata fields
    data['metadata']['number_of_collections'] += 1
    data['metadata']['collections'].append(collection_name.lower().replace(" ", "_"))
    
    # Create a list entry for the newly created collection
    new_collection = {
        'collection_name': collection_name.lower().replace(" ", "_"),
        'date_created': current_timestamp,
        'date_last_modified': current_timestamp,
        'files': [str(file) for file in collection_path.iterdir()]
    }
    data['collections'].append(new_collection)
    
    # Overwrite datashelf_metadata.yaml with new metadata
    with open(datashelf_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)
        
    return 0

# Update file list of collection in datashelf metadata when a file is saved - Used inside save()
def _update_datashelf_metadata_collection_files(collection_name:str, collection_path:str):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    collection_files = _get_collection_files(collection_name = collection_name)
    collection_file_names = [file['name'] for file in collection_files if file['deleted'] == False]
    datashelf_metadata_path = Path(collection_path).parent / 'datashelf_metadata.yaml'
    
    with open(datashelf_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    for _, collection in enumerate(data['collections']):
        if collection.get('collection_name') == collection_name.lower().replace(" ", "_"):
            collection['date_last_modified'] = current_timestamp
            collection['files'] = collection_file_names
        else:
            pass
    
    with open(datashelf_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)
        
# General-purpose edit function - UNUSED
def _edit_datashelf_metadata(collection_name:str, update:dict):
    """
    Find .datashelf directory, check that update dictionary is valid, open datashelf metadata, 
    loop through to find the correct collection entry, loop through update dictionary and assign 
    new values to key in collection dictionary. Write updated dictionary of dictionaries back to YAML metdata file.

    Args:
        collection_name (str): Name of the collection you want to edit.
        update (dict): A dictionary containing the edited values and their corresponding keys.

    Raises:
        ValueError: If a key in your update dictionary does not match the allowed keys as specified in the function, an error will be thrown. 
    """
    # Check if update dict is valid
    update_keys = [key for key,value in update.items()]
    if not set(update_keys).issubset(set(["collection_name", "date_created", "files"])):
        raise ValueError("Invalid key detected in update arg. Update can only have the following keys:\n\t-collection_name\n\t-date_created\n\t-files.")
    
    import yaml
    from datetime import datetime
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    metadata_path = os.path.join(datashelf_path,'datashelf_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read metadata file
    with open(metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Loop through collection entries, find one that matches name arg, update it using update dict
    for _, collection in enumerate(data['collections']):
        if collection.get('collection_name').lower().replace(" ", "_") == collection_name.lower().replace(" ", "_"):
            collection["date_last_modified"] = current_timestamp
            for key, value in update.items():
                try:
                    collection[key] = value
                except Exception as e:
                    logger.error(f"An error occured: {e}")
        else:
            pass
        
    # Overwrite datashelf_metadata.yaml with updated data
    with open(metadata_path, 'w') as f:
        yaml.safe_dump(data, f)
        
# Remove collection file if deleted

# Update metadata to remove deleted file


################################################################################
# Collection-level metadata helpers
################################################################################

# Initialize collection metadata file
def _initialize_collection_metadata(collection_name:str):
    """_summary_

    Args:
        collection_name (str): _description_

    Returns:
        _type_: _description_
    """
    
    # Get path variables
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    collection_path = datashelf_path/collection_name.lower().replace(" ", "_")
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create metadata structure
    files = [f'{collection_name.lower().replace(" ", "_")}_metadata.yaml']
    num_files = len(files)
    
    metadata = {}
    metadata['metadata'] = {'collection_name': collection_name.lower().replace(" ", "_"),
                          'date_created': current_timestamp,
                          'number_of_files': num_files,
                          'most_recent_commit': "",
                          'max_version':0
                          }
    metadata['files'] = [{'name':f'{collection_name.lower().replace(" ", "_")}_metadata.yaml' ,
                                  'hash':"",
                                  'date_created': current_timestamp,
                                  'date_last_modified': "",
                                  'tag': "",
                                  'version': None,
                                  'message': "",
                                  'file_path': str(collection_metadata_path),
                                  'deleted':False
                                  }]
    
    # Write metadata to collection_metadata_path
    with open(collection_metadata_path, 'w') as f:
            yaml.safe_dump(metadata, f, sort_keys = False)
    return 0

# Read latest version number in metadata and increment by 1 - Used in save()
def _get_next_version_number(collection_name:str, collection_path:str):
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    files = _get_collection_files(collection_name = collection_name)
    
    if len(files) < 1:
        raise ValueError(f"No metadata found for collection: {collection_name}."
                         f"Your collection may be corrupted. Consider deleting and re-creating the collection.")
    
    if data.get('metadata', {}).get('max_version', 0) == 0:
        return 1
    
    else:
        return data['metadata']['max_version'] + 1

# Add a file entry to collection metadata file- Used in save()
def _add_file_to_collection_metadata(collection_name:str, file_name:str, tag:str, message:str, df_hash:str, version:int, file_path:str):
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    collection_path = datashelf_path/collection_name.lower().replace(" ", "_")
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Idk if I need to check that file isn't empty. It shouldn't be based on the way init() and create_collection() work
    file_metadata = {
        'name':file_name,
        'hash':df_hash,
        'date_created':current_timestamp,
        'date_last_modified':current_timestamp,
        'tag':tag,
        'version':version,
        'message':message,
        'file_path':str(file_path),
        'deleted':False
    }
    
    data['files'].append(file_metadata)
    
    with open(collection_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)

# Update metadata field of collection metadata file - Used in save()
def _update_collection_metadata_info(collection_name:str, saved_df_file_path:str, new_version:int):
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    collection_path = datashelf_path/collection_name.lower().replace(" ", "_")
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    
    data['metadata']['number_of_files'] += 1
    data['metadata']['most_recent_commit'] = saved_df_file_path
    data['metadata']['max_version'] = new_version
    
    with open(collection_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)
    
    return 0

# General-purpose edit funciton for collection metadata - UNUSED
def _edit_collection_metadata(collection_name:str, update:dict, config_or_files:Literal['config', 'files']):
    """_summary_

    Args:
        update (dict): _description_
    """
    
    # Check that update dict is valid
    update_keys = [key for key,value in update.items()]
    if not set(update_keys).issubset(set(["most_recent_commit", "number_of_files", "message", "name", "tag"])):
        raise ValueError("Invalid key detected in update arg. Update can only have the following:\nFor updating config:\n\t-most_recent_commit\n\t-number_of_files\nFor updating files:\n\t-message\n\t-name\n\t-tag")
    
    import yaml
    from datetime import datetime
    
    collection_path = os.path.join(_find_datashelf_root(return_datashelf_path = True), collection_name.lower().replace(" ", "_"))
    collection_metadata_path = os.path.join(collection_path,f'{collection_name.lower().replace(" ", "_")}_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read metadata file
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    if config_or_files == 'config':
        # Loop through collection entries, find one that matches name arg, update it using update dict
        for _, collection in enumerate(data['config']):
            collection["date_last_modified"] = current_timestamp
            collection["number_of_files"] += 1
            for key, value in update.items():
                try:
                    collection[key] = value
                except Exception as e:
                    logger.error(f"An error occured: {e}")
                    raise
    
    # I don't think there's a use case for this option right now so I'll leave it for later
    elif config_or_files == 'files':
        ...
    
    # Error handling for incorrect value of config_or_files
    else:
        raise ValueError("Invalid argument for config_or_files, must be either 'config' or 'files'.")

        
    # Overwrite datashelf_metadata.yaml with updated data
    with open(collection_metadata_path, 'w') as f:
        yaml.safe_dump(data, f)