import yaml
from pathlib import Path
import shutil
import pandas as pd
from datashelf.utils.tools import _find_datashelf_root
from datashelf.utils.logging import setup_logger

logger = setup_logger(__name__)

def checkout(collection_name:str, hash_value:str):
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    collection_path = datashelf_path/f'{collection_name.lower().replace(" ", "_")}'
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    dest_path = datashelf_path.parent
    
    with open(collection_metadata_path, 'r') as f:
        data = yaml.safe_load(f)
    
    for _, file in enumerate(data['files']):
        if file.get("hash") == hash_value:
            source_file = Path(file["file_path"])
            shutil.copy(source_file, dest_path/source_file.name)
            return 0
        else:
            pass

    
def load(collection_name:str, hash_value:str):
    datashelf_path = _find_datashelf_root(return_datashelf_path = True)
    collection_path = datashelf_path/f'{collection_name.lower().replace(" ", "_")}'
    collection_metadata_path = collection_path/f'{collection_name.lower().replace(" ", "_")}_metadata.yaml'
    
    with open(collection_metadata_path, 'r') as f:
       data = yaml.safe_load(f)
       
    for _, file in enumerate(data['files']):
        if file.get("hash") == hash_value:
            file_ext = Path(file['file_path']).suffix
            
            if file_ext == ".csv":
                return pd.read_csv(file['file_path'])
            else:
                return pd.read_parquet(file['file_path']) 