import os
from pathlib import Path
import yaml
from datetime import datetime
from datashelf.utils.tools import _get_collection_files, _find_datashelf_root
from datashelf.utils.logging import setup_logger

logger = setup_logger(__name__)
   
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
    

