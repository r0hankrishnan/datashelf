import yaml
import pathlib
from pathlib import Path
from typing import Union
from datetime import datetime
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.logging import setup_logger
from datashelf.utils.tools import _get_collection_files

logger = setup_logger(__name__)

# --- Top-level datashelf metadata helpers ---
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
        
# Remove collection file if deleted

# Update metadata to remove deleted file
        
# --- Collection-level metadata helpers ---

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