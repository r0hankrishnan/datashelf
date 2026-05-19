import pandas as pd
from pathlib import Path
from datashelf.core.directory import find_datashelf_path
from datashelf.core.metadata import load_metadata, FileEntry
from datashelf.core.config import get_parquet_engine
from datashelf.core.lookup import find_matches

class AmbiguousLookupError(Exception):
    def __init__(self, lookup_key: str, matches: list[FileEntry]):
        self.lookup_key = lookup_key
        self.matches = matches
        super().__init__(f"More than one match found for {lookup_key}")
    

# =============================================================
# MAIN FUNCTION
# =============================================================
def load(lookup_key: str, to_df: bool = False) -> Path | pd.DataFrame:
    """Load a stored artifact from the datashelf.

    Resolves the lookup key against stored metadata by checking dataset name first,
    then hash prefix, then exact hash. Returns the artifact as a file path or 
    pandas DataFrame depending on the value of to_df.

    Args:
        lookup_key (str): Dataset name, full hash, or unique hash prefix to look up in the metadata.
        to_df (bool, optional): Whether to load the artifact into a pandas DataFrame. Defaults to False.

    Raises:
        ValueError: If no matching dataset is found for the lookup key.
        AmbiguousLookupError: If multiple matching datasets are found. Contains the matches
            as structured data for callers that need to handle ambiguity programmatically.
        RuntimeError: If an unexpected state is encountered during resolution.

    Returns:
        Path | pd.DataFrame: The resolved artifact path, or a pandas DataFrame if to_df is True.
    """
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path=datashelf_path)
    
    name_match, hash_approx_match, hash_exact_match = find_matches(lookup_key = lookup_key, metadata = metadata)
    
    entry = _resolve_matches(lookup_key = lookup_key, name_match = name_match, hash_approx_match = hash_approx_match, 
                           hash_exact_match = hash_exact_match)

    engine = get_parquet_engine(datashelf_path=datashelf_path)
    full_path = datashelf_path / entry["stored_path"]
    
    return full_path if not to_df else pd.read_parquet(full_path, engine=engine)

# =============================================================
# HELPER FUNCTIONS
# =============================================================
def _resolve_matches(lookup_key: str, name_match: list[FileEntry], hash_approx_match: list[FileEntry], 
                   hash_exact_match: list[FileEntry]) -> FileEntry:
    """Resolves match lists returned by find_matches() into a single FileEntry.

    Checks match lists in priority order: name matches first, then approximate
    hash matches, then exact hash matches. Raises if no matches are found or
    if any match list is ambiguous (more than one result).

    Args:
        lookup_key (str): The original lookup key, used for error messages.
        name_match (list[FileEntry]): Entries whose name equals the lookup key.
        hash_approx_match (list[FileEntry]): Entries whose hash starts with the lookup key.
        hash_exact_match (list[FileEntry]): Entries whose hash exactly equals the lookup key.

    Raises:
        ValueError: If no matches are found across all three match lists.
        AmbiguousLookupError: If name_match or hash_approx_match contains more than one entry.
        RuntimeError: If all match lists are exhausted without returning — should never occur.

    Returns:
        FileEntry: The single resolved metadata entry.
    """
    if len(name_match) == 0 and len(hash_approx_match) == 0 and len(hash_exact_match) == 0:
        raise ValueError(f"No match found for {lookup_key}. Use the `list` command to see available datasets in .datashelf/.")
    
    if len(name_match) > 1:
        raise AmbiguousLookupError(lookup_key = lookup_key, matches = name_match)
    
    if len(name_match) == 1:
        return name_match[0]
    
    if len(hash_approx_match) > 1:
        raise AmbiguousLookupError(lookup_key = lookup_key, matches = hash_approx_match)
    
    if len(hash_approx_match) == 1:
        return hash_approx_match[0]
        
    if len(hash_exact_match) == 1:
        return hash_exact_match[0]
     
    raise RuntimeError("Unreachable state in `load()`.") # Only raises if all checks fail -- which should not be possible

