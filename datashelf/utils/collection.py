import os
import yaml
from datetime import datetime
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.logging import setup_logger
from typing import Literal

logger = setup_logger(__name__)

# Should rework this function to directly take in the data that is loaded in _get_collection_files
# that way, we don't have to open the metadata file twice to get the same info.
def _add_file_to_collection_metadata(collection_name, file_name:str, tag:str, message:str, file_hash:str = "", version:float = None):
    import yaml
    from datetime import datetime
    
    collection_path = os.path.join(_find_datashelf_root(return_datashelf_path = True), collection_name.lower().replace(" ", "_"))
    collection_metadata_path = os.path.join(collection_path,f'{collection_name.lower().replace(" ", "_")}_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Idk if I need to check that file isn't empty. It shouldn't be based on the way init() and create_collection() work
    file_metadata = {
        'name':file_name,
        'hash':file_hash, # Maybe for future versions idk yet
        'date_created':current_timestamp,
        'date_last_modified':current_timestamp,
        'tag':tag,
        'version':version, #For future versions with better tracking
        'message':message
    }
    data['files'].append(file_metadata)
    
    with open(collection_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)


def _update_config_metadata(collection_name:str, most_recent_commit:str):
    import yaml
    from datetime import datetime
    
    # Get collection and metadata paths, store current timestamp
    collection_path = os.path.join(_find_datashelf_root(return_datashelf_path = True), collection_name.lower().replace(" ", "_"))
    collection_metadata_path = os.path.join(collection_path,f'{collection_name.lower().replace(" ", "_")}_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open metadata with metadata path
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Get and updateconfig entries
    for _, config in enumerate(data['config']):
        config["date_last_modified"] = current_timestamp
        config["number_of_files"] += 1
        config["most_recent_commit"] = most_recent_commit
    
    # Write entire metadata file back to metadata path
    with open(collection_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)

### IDK IF I'LL BE USING THE FUNCTIONS BELOW ###
    
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