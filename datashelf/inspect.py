from datashelf.core.directory import find_datashelf_path
from datashelf.core.metadata import load_metadata, FileEntry
from datashelf.core.config import get_config_tags_settings, validate_tags
from datashelf.core.lookup import find_matches

# =============================================================
# MAIN FUNCTIONS
# =============================================================
def ls(filter_tag: list[str] | None = None) -> list[FileEntry]:
    """Print a table of datasets currently registered in .datashelf.

    Args:
        filter_tag (list[str] | None, optional): Optional list of tags to filter displayed datasets. Defaults to None.
    """
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path=datashelf_path)
    enforce_tags, allowed_tags = get_config_tags_settings(datashelf_path=datashelf_path)

    entries = metadata["files"]

    if filter_tag:
        if isinstance(filter_tag, str):
            filter_tag = [filter_tag]

        if enforce_tags:
            for tag in filter_tag:
                validate_tags(tag=tag, allowed_tags=allowed_tags)

        entries = [entry for entry in entries if entry["tag"] in filter_tag]

    if not entries:
        return []
    
    return entries

def show(lookup_key: str) -> list[FileEntry]:
    """Print detailed metadata information for a specific dataset identified by the lookup key.
    The lookup key can be a dataset name, full hash, or unique hash prefix. If multiple matches are found for the lookup key,
    metadata information for all matching datasets will be displayed.

    Args:
        lookup_key (str): Dataset name, full hash, or unique hash prefix to look up in the metadata.

    Raises:
        ValueError: If no matching dataset is found.
        RuntimeError: If an unexpected state is encountered.
    """
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path=datashelf_path)
    
    name_match, hash_approx_match, hash_exact_match = find_matches(lookup_key = lookup_key, metadata = metadata)
    
    if len(name_match) == 0 and len(hash_approx_match) == 0 and len(hash_exact_match) == 0:
        raise ValueError(f"No match found for {lookup_key}. Use the `list` command to see available datasets in .datashelf/.")
    
    if len(name_match) > 0:
        return name_match
    
    if len(hash_approx_match) > 0:
        return hash_approx_match
    
    if len(hash_exact_match) > 0:
        return hash_exact_match
    
    raise RuntimeError(f"Unreachable state in `show()`.")


# =============================================================
# HELPER FUNCTIONS
# =============================================================
def _truncate(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[: max_len - 3] + "..."