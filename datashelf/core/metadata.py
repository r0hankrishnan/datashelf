import json
from pathlib import Path
from datetime import datetime

FileEntry = dict[str,str]
Metadata = dict[str,float | list[FileEntry]]

def init_metadata(datashelf_path:Path):
    metadata: Metadata = {}
    metadata["schema_version"] = 0.10
    metadata["Files"] = []
    metadata["Files"].append({
        "File Name": "config.yaml",
        "File Hash": "",
        "Message": "DataShelf configuration file.",
        "Tag": "",
        "Date Added": datetime.now().replace(microsecond=0).isoformat()

    })
    
    with open(datashelf_path / "metadata.json", "w") as metadata_file:
        json.dump(metadata, metadata_file)