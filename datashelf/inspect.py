from pathlib import Path
from datashelf.core.directory import find_datashelf_path
from datashelf.core.metadata import load_metadata, FileEntry
from datashelf.core.config import get_config_tags_settings, validate_tags

MAX_MSG = 60
HASH_WIDTH = 8

def ls(filter_tag: list[str] | None = None):
    """Print a table of datasets currently registered in .datashelf.

    Args:
        filter_tag (list[str] | None, optional): Optional list of tags to filter displayed datasets. Defaults to None.
    """
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path=datashelf_path)
    enforce_tags, allowed_tags = get_config_tags_settings(datashelf_path = datashelf_path)
    
    files = metadata["files"]
    
    if filter_tag:
        if isinstance(filter_tag, str):
            filter_tag = [filter_tag]
            
        if enforce_tags:
            for tag in filter_tag:
                validate_tags(tag = tag, allowed_tags = allowed_tags)
            
        files = [f for f in files if f["tag"] in filter_tag]
        
    if not files:
        print("No matching metadata found.")
        return
    
    _print_metadata_table(files = files)
    
def show(lookup_key: str) -> None:
    datashelf_path = find_datashelf_path()
    metadata = load_metadata(datashelf_path = datashelf_path)
        
    name_matches = [file_entry for file_entry in metadata["files"] if file_entry["name"] == lookup_key]
    hash_approx_match = [file_entry for file_entry in metadata["files"] 
                         if file_entry["file_hash"].startswith(lookup_key) and file_entry["file_hash"] != lookup_key]
    hash_exact_match = [file_entry for file_entry in metadata["files"] if file_entry["file_hash"] == lookup_key]

    # First check name, then approx hash, then exact hash
    if len(name_matches) == 0 and len(hash_exact_match) == 0 and len(hash_approx_match) == 0:
        raise ValueError(f"No match found for {lookup_key}. Use the `list` command to see available datasets in .datashelf/.")
    
    elif len(name_matches) > 1:
        entry_str = f"Multiple matches found for '{lookup_key}'. Displaying all matches:\n\n"
        
        for file_entry in name_matches:
            entry_str += _create_metadata_entry_str(entry = file_entry)
        
    elif len(name_matches) == 1:
        file_entry = name_matches[0]
        entry_str = _create_metadata_entry_str(entry = file_entry)
        
    elif len(hash_approx_match) > 1:        
        entry_str = f"Multiple matches found for '{lookup_key}'. Displaying all matches:\n\n"
        
        for file_entry in hash_approx_match:
            entry_str += _create_metadata_entry_str(entry = file_entry)
              
    elif len(hash_approx_match) ==1:
        file_entry = hash_approx_match[0]
        entry_str = _create_metadata_entry_str(entry = file_entry)

    elif len(hash_exact_match) == 1:
        file_entry = hash_exact_match[0]
        entry_str = _create_metadata_entry_str(entry = file_entry)

    else:
        raise RuntimeError(f"Unreachable state in `show()`.")
    
    print(entry_str)
    
def _truncate(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[:max_len - 3] + "..."

def _print_metadata_table(files: list[FileEntry]) -> None:

    name_width = max(len("Name"), max(len(f["name"]) for f in files))
    tag_width = max(len("Tag"), max((len(f.get("tag") or "") for f in files), default=0))
    msg_width = max(
        len("Message"),
        max(len(_truncate(f["message"] or "", MAX_MSG)) for f in files)
    )

    print(
        f"{'Hash':<{HASH_WIDTH}}  "
        f"{'Name':<{name_width}}  "
        f"{'Tag':<{tag_width}}  "
        f"{'Message':<{msg_width}}"
    )

    print("-" * (HASH_WIDTH + name_width + tag_width + msg_width + 6))

    for entry in files:
        print(
            f"{entry['file_hash'][:8]:<{HASH_WIDTH}}  "
            f"{entry['name']:<{name_width}}  "
            f"{entry['tag']:<{tag_width}}  "
            f"{_truncate(entry['message'] or '', MAX_MSG):<{msg_width}}"
        )
        
def _create_metadata_entry_str(entry: FileEntry) -> str:
    fields = {
        "Hash": entry["file_hash"],
        "Name": entry["name"],
        "Tag": entry["tag"],
        "Message": entry["message"],
        "Stored at": entry["stored_path"],
        "Added": entry["datetime_added"],
    }

    label_width = max(len(label) for label in fields)
    lines = [f"{label:<{label_width}}  {value}" for label, value in fields.items()]
    width = max(len(line) for line in lines)
    msg = "-" * width + "\n"
    msg += "\n".join(lines)
    msg += "\n" + "-" * width + "\n\n"
    
    return msg
        