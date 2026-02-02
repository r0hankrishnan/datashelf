import yaml
from pathlib import Path
from save import _get_file_names

def _get_allowed_tags(datashelf_path: Path):
    with open(datashelf_path / "config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)["Config"]
        
    if config["Enforce CCDS Tags"]:
        return config["Enforce CCDS Tags"], config["Allowed Tags"]
    else:
        return config["Enforce CCDS Tags"], None

def _get_datashelf_path():
    
    current_path = Path.cwd()
    
    while current_path != current_path.parent:
        if (current_path / ".datashelf").exists():
            return current_path / ".datashelf"
        else:
            current_path = current_path.parent
    
    return None
    
def _insert_metadata_entry(datashelf_path:Path,
                          file_name:str,
                          file_hash:str,
                          message:str,
                          tag:str,
                          date_added:str):
    # Create dict payload
    metadata_entry = {
        "File Name": file_name,
        "File Hash": file_hash,
        "Message": message,
        "Tag": tag,
        "Date Added": date_added
    }
    
    # Open & read metadata
    with open(datashelf_path / "metadata.yaml", 'r') as f:
        metadata = yaml.safe_load(f)
    
    # Add some checks here so we aren't opening and closing the file more than needed
    if file_name in _get_file_names(datashelf_path = datashelf_path):
        raise ValueError("File Name must not already exist in metadata.")
    
    enforce_tags, allowed_tags = _get_allowed_tags(datashelf_path = datashelf_path)
    
    if enforce_tags:
        if tag not in allowed_tags:
            raise ValueError(f"Tag must be on of {', '.join(allowed_tags)}")
    # Append payload to "Files"
    metadata["Files"].append(metadata_entry)