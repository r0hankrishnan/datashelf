from pathlib import Path

def init_datashelf_directory(datashelf_path:Path):
    # Check if datashelf already exists at path -> else make .datashelf/ directory
        if datashelf_path.exists(): # should this raise an exception?
            print(f"Datasehlf already initialized at {str(datashelf_path)}")
        
        else:
            datashelf_path.mkdir()
            
def find_datashelf_path() -> Path | None:
    curr_path = Path().cwd()
    
    while curr_path != curr_path.parent:
        if (curr_path / ".datashelf").exists():
            return (curr_path/".datashelf")
        else:
            curr_path = curr_path.parent
    
    return None

