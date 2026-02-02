from pathlib import Path
import yaml
from datetime import datetime

def init(custom_path:str|None = None):
    if custom_path:
        if not Path(custom_path).exists():
            raise NotADirectoryError(f"Could not find {custom_path}. Please enter an existing path within your project.")
        
        datashelf_path:Path = Path(custom_path) / ".datashelf"
        
        _init_datashelf_directory(datashelf_path = datashelf_path)
        # init_config_and_metadata(datashelf_path = datashelf_path)
        _init_config(datashelf_path = datashelf_path)
        _init_metadata(datashelf_path = datashelf_path)
    
    else:
        cwd:Path = Path().cwd()    
        datashelf_path:Path = cwd / ".datashelf"
        
        _init_datashelf_directory(datashelf_path = datashelf_path)
        # init_config_and_metadata(datashelf_path = datashelf_path)
        _init_config(datashelf_path = datashelf_path)
        _init_metadata(datashelf_path = datashelf_path)

def _init_datashelf_directory(datashelf_path:Path):
    # Check if datashelf already exists at path -> else make .datashelf/ directory
        if datashelf_path.exists(): # should this raise an exception?
            print(f"Datasehlf already initialized at {str(datashelf_path)}")
        
        else:
            datashelf_path.mkdir()
       
def _init_config(datashelf_path:Path):
    # Set up config file
    config:dict[str, dict[str, bool | list[str]]] = {}
    config["Config"] = {
        "Enforce CCDS Tags": True,
        "Allowed Tags": ["raw", "external", "intermediate", "processed"]
    }
    
    with open(datashelf_path/"config.yaml", "w") as config_file:
        yaml.safe_dump(config, config_file, sort_keys = False)

def _init_metadata(datashelf_path:Path):
    metadata:dict[str, list[dict[str,str]]] = {}
    metadata["Files"] = []
    metadata["Files"].append({
        "File Name": "config.yaml",
        "File Hash": "",
        "Message": "DataShelf configuration file.",
        "Tag": "",
        "Date Added": str(datetime.now())
    })
    
    with open(datashelf_path / "metadata.yaml", "w") as metadata_file:
        yaml.safe_dump(metadata, metadata_file, sort_keys = False)
        

# DEPRECATED
def init_config_and_metadata(datashelf_path:Path):
    # Set up config file
    config:dict[str, dict[str, bool | list[str]]] = {}
    config["Config"] = {
        "Enforce CCDS Tags": True,
        "Allowed Tags": ["raw", "external", "intermediate", "processed"]
    }
    
    with open(datashelf_path/"config.yaml", "w") as f:
        yaml.safe_dump(config, f, sort_keys = False)
        
    # Set up metadata file
    metadata:dict[str, list[dict[str, str]]] = {}
    metadata["Files"] = []
    metadata["Files"].append({
        "File Name": "config.yaml",
        "File Hash": "",
        "Message": "DataShelf configuration file.",
        "Tag": "",
        "Date Added": str(datetime.now())
    })
    
    with open(datashelf_path / "metadata.yaml", "w") as f:
        yaml.safe_dump(metadata, f, sort_keys = False)