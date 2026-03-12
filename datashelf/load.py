import pandas as pd
from pathlib import Path
from datashelf.core.directory import find_datashelf_path
from datashelf.core.metadata import load_metadata
from datashelf.core.config import get_parquet_engine

def load(lookup_key: str, to_df: bool = False) -> Path | pd.DataFrame:
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path = datashelf_path)
        
    name_matches = [entry_file for entry_file in metadata["files"] if entry_file["name"] == lookup_key]
    hash_exact_match = [entry_file for entry_file in metadata["files"] if entry_file["file_hash"] == lookup_key]
    hash_approx_match = [entry_file for entry_file in metadata["files"] 
                         if entry_file["file_hash"].startswith(lookup_key) and entry_file["file_hash"] != lookup_key]
    
    # First check name, then exact hash, then approx hash
    if len(name_matches) == 0 and len(hash_exact_match) == 0 and len(hash_approx_match) == 0:
        raise ValueError(f"No match found for {lookup_key}. Use the `list` command to see available datasets in .datashelf/.")
    
    elif len(name_matches) > 1:
        msg = (
            f"More than one match found for {lookup_key}:"
        )
        
        for file_entry in name_matches:
            msg += (f"\n\nFile Hash: {file_entry['file_hash']} | Name: {file_entry['name']} | Message: {file_entry['message']} | "
                    f"Tag: {file_entry['tag']}")
        
        msg += "Please refer to the entries above, copy the appropriate file hash, and run `load` again with the file hash."
        raise ValueError(msg)
        
    elif len(name_matches) == 1:
        file_entry = name_matches[0]
    
    elif len(hash_exact_match) == 1:
        file_entry = hash_exact_match[0]
    
    elif len(hash_approx_match) > 1:
        msg = (
            f"More than one match found for {lookup_key}:"
        )
        
        for file_entry in hash_approx_match:
            msg += (f"\n\nFile Hash: {file_entry['file_hash']} | Name: {file_entry['name']} | Message: {file_entry['message']} | "
                    f"Tag: {file_entry['tag']}")
        
        msg += "Please refer to the entries above, copy the appropriate file hash, and run `load` again with the file hash."
        raise ValueError(msg)
        
    elif len(hash_approx_match) ==1:
        file_entry = hash_approx_match[0]
    
    else:
        raise RuntimeError(f"Unreachable state in `load()`.")
    
    engine = get_parquet_engine(datashelf_path = datashelf_path)
    full_path = datashelf_path / file_entry["stored_path"]
    return full_path if not to_df else pd.read_parquet(full_path, engine = engine)