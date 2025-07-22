import os
import logging
from datashelf.utils.tools import _get_collection_files, _find_datashelf_root
from datashelf.utils.logging import setup_logger

logger = setup_logger(__name__)

def _make_datashelf_metadata_structure():
    import yaml
    from datetime import datetime
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    datashelf_metadata_path = os.path.join(datashelf_path, 'datashelf_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    collections = [collection for collection in os.listdir(datashelf_path) if collection not in 'datashelf_metadata.yaml']
    number_of_collections = len(collections)
    
    new_metadata = {}
    new_metadata['config'] = [{'date_created': current_timestamp,
                        'date_created': current_timestamp,
                        'number_of_collections': number_of_collections,
                        'collections': collections
                        }]
    new_metadata['collections'] = []
    
    with open(datashelf_metadata_path, 'w') as f:
        yaml.safe_dump(new_metadata, f, sort_keys = False)
        

def _add_collection_to_datashelf_metadata(collection_name:str):
    ...

# This is only run in datashelf.core.save()
def _update_datashelf_metadata_with_added_collection(collection_name:str):
    import yaml
    from datetime import datetime
    
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    datashelf_metadata_path = os.path.join(datashelf_path, 'datashelf_metadata.yaml')
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    with open(datashelf_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    data['config'][0]['number_of_collections'] += 1
    data['config'][0]['collections'].append(collection_name.lower().replace(" ", "_"))
    
    collection_path = os.path.join(datashelf_path, collection_name.lower().replace(" ", "_"))

    new_collection = {
        'collection_name':collection_name.lower().replace(" ", "_"),
        'date_created':current_timestamp,
        'date_last_modified':current_timestamp,
        'files':[file for file in os.listdir(collection_path)]
    }
    
    data['collections'].append(new_collection)
    
    with open(datashelf_metadata_path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)
    
def _update_datashelf_metadata_with_added_file_in_collection(collection_name:str, collection_path:str):
    import yaml
    from datetime import datetime
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    collection_files = _get_collection_files(collection_name = collection_name)
    collection_file_names = [file['name'] for file in collection_files]
    
    with open(os.path.join(collection_path, '../datashelf_metadata.yaml')) as f:
        data = yaml.safe_load(f)
        
    # update to collections[idx][files] and update last_modified with timestamp
    for _, collection in enumerate(data['collections']):
        if collection.get('collection_name') == collection_name.lower().replace(" ", "_"):
            collection['date_last_modified'] = current_timestamp
            collection['files'] = collection_file_names
        else:
            pass
    
    with open(os.path.join(collection_path, '../datashelf_metadata.yaml'), 'w') as f:
        yaml.safe_dump(data, f, sort_keys = False)
    
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
    

