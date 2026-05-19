from datashelf.core.metadata import Metadata, FileEntry

def find_matches(lookup_key: str, metadata: Metadata) -> tuple[list[FileEntry],list[FileEntry], list[FileEntry]]:
    name_match = [file_entry for file_entry in metadata["files"] if file_entry["name"] == lookup_key]
    hash_approx_match = [file_entry for file_entry in metadata["files"] if file_entry["file_hash"].startswith(lookup_key) 
                         and file_entry["file_hash"] != lookup_key]
    hash_exact_match = [file_entry for file_entry in metadata["files"] if file_entry["file_hash"] == lookup_key]
    
    return name_match, hash_approx_match, hash_exact_match