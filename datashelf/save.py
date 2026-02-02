from pathlib import Path
import yaml
from datetime import datetime

# Save only used INSIDE a jupyter notebook -> otherwise would use load in CLI
# To save a dataset:
    # Compile user-generated info like 
    
def _get_file_names(datashelf_path:Path):
    # Make sure path exists
    if not datashelf_path.exists():
        raise FileNotFoundError(f"No .datashelf directory found at {datashelf_path}")
    
    # Load YAML and compile list of file names
    with open(".datashelf/metadata.yaml", "r") as f:
        metadata = yaml.safe_load(f)
    
    file_list = []
    for file in metadata["Files"]:
        file_list.append(file["File Name"])
    
    return file_list[]