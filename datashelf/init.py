from pathlib import Path
import yaml
from datetime import datetime

def initialize_datashelf(custom_path: str = None):
    # Naive implementation where we just do all of the operations in the function
    # Should pull out specific actions into their own functions eventually
    
    ## NOTES:
    
    # The only reason for the highest-level if statement is the differing `datashelf_path` variable
    # We should pull everything else into a function that takes `datashelf_path` as an arg
    # The creation of the config and metadata are the same regardless of the value of `datashelf_path`
    # so it should also be a separate function with no args
    
    # If the user wants to initialize in a particular path
    if custom_path:
        datashelf_path = Path(custom_path) / ".datashelf"
        
        # This is repeated between custom_path and no custom_path -> 
        # should pull out into its own function(s)
        
        # Check if custom path DataShelf alread exists
        if datashelf_path.exists():
            print(f"Datasehlf already initialized at {str(datashelf_path)}")
        
        else:
            datashelf_path.mkdir()
            
            # Set up config file
            config = {
                "Enforce CCDS Tags": True,
                "Allowed Tags": ["raw", "external", "intermediate", "processed"]
            }
            
            with open(datashelf_path/"config.yaml", "w") as f:
                yaml.safe_dump(config, f, sort_keys = False)
                
            # Set up metadata file
            metadata = {
                "File Name": "config.yaml",
                "File Hash": "",
                "Message": "DataShelf configuration file.",
                "Tag": "",
                "Date Added": str(datetime.now())
            }
            
            with open(datashelf_path / "metadata.yaml", "w") as f:
                yaml.safe_dump(metadata, f, sort_keys = False)
                
    # Initialize in current working directory
    else:
        cwd = Path().cwd()    
        datashelf_path = cwd / ".datashelf"
        
        if datashelf_path.exists():
            print(f"Datasehlf already initialized at {str(datashelf_path)}.")
        
        else:
            datashelf_path.mkdir()
            
            # Set up config file
            config = {
                "Enforce CCDS Tags": True,
                "Allowed Tags": ["raw", "external", "intermediate", "processed"]
            }
            
            with open(datashelf_path/"config.yaml", "w") as f:
                yaml.safe_dump(config, f, sort_keys = False)
                
            # Set up metadata file
            metadata = {
                "File Name": "config.yaml",
                "File Hash": "",
                "Message": "DataShelf configuration file.",
                "Tag": "",
                "Date Added": str(datetime.now())
            }
            
            with open(datashelf_path / "metadata.yaml", "w") as f:
                yaml.safe_dump(metadata, f, sort_keys = False)
                
            