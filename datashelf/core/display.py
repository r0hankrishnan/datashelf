from typing import Literal
from tabulate import tabulate
import yaml
from datashelf.utils.logging import setup_logger
from datashelf.utils.tools import _find_datashelf_root


logger = setup_logger(__name__)

def ls(to_display = Literal["ds-md", "ds-coll", "coll-md", "coll-files"]):
    if to_display in ["ds-md", "ds-coll", "coll-md", "coll-files"]:
    
        if to_display == "ds-md":
            _display_datashelf_metadata(field = "metadata")
            
        elif to_display == "ds-coll":
            _display_datashelf_metadata(field = "collections")
        
        elif to_display == "coll-md":
            collection_name = input("Collection name? ")
            _display_collection_metadata(collection_name = collection_name, field = "metadata")
        
        else:
            collection_name = input("Collection name? ")
            _display_collection_metadata(collection_name = collection_name, field = "files" )
            
    else:
        err_msg = (f'{to_display} is not a valid value for to_display.'
                   'Please select one of the following based on what you want to display:\n'
                   '\tdatashelf_metadata.yaml "metadata": "ds-md"'
                   '\n\tdatashelf_metadata.yaml "collections": "ds-coll"'
                   '\n\t{collection_name}_metadata.yaml "metadata": "coll-md"'
                   '\n\t{collection_name}_metadata.yaml "files": "coll-files"'
        )
        logger.error(err_msg)
        raise ValueError(err_msg)

def _display_datashelf_metadata(field = Literal['metadata', 'collections']):
    
    if field not in ['metadata', 'collections']:
        err_msg = f'field must be either "metadata" or "collections". {field} is invalid.'
        logger.error(err_msg)
        raise ValueError(err_msg)
    try:
        datashelf_path = _find_datashelf_root(return_datashelf_path=True)
        datashelf_metadata_path = datashelf_path/'datashelf_metadata.yaml'
    except Exception as e:
        err_msg = f"An error occured. Make sure you are in the same directory as your .datashelf folder."
        logger.error(err_msg)
        raise ValueError(e)       
    with open(datashelf_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    print("hi")

    if field == 'metadata':
            print(tabulate([data['metadata']], headers = "keys", tablefmt = "grid"))
        
    else:
        print(tabulate(data['collections'], headers = "keys", tablefmt = "grid"))
    
        

def _display_collection_metadata(collection_name:str, field = Literal['metadata', 'files']):
    if field not in ['metadata', 'files']:
        err_msg = f'field must be either "metadata" or "files". {field} is invalid.'
        logger.error(err_msg)
        raise ValueError(err_msg)
    
    try:
        datashelf_path = _find_datashelf_root(return_datashelf_path=True)
        collection_path = datashelf_path/collection_name.lower().replace(" ", "_")
        collection_metadata_path = collection_path/f'{collection_name.strip().lower().replace(" ", "_")}_metadata.yaml'
    except Exception as e:
        err_msg = f"An error occured. Make sure you are in the same directory as your .datashelf folder."
        logger.error(err_msg)
        raise ValueError(e)    
    
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
        
    if field == 'metadata':
        print(tabulate([data['metadata']], headers = "keys", tablefmt = "grid"))
    
    else:
        print(tabulate(data['files'], headers = "keys", tablefmt = "grid"))
