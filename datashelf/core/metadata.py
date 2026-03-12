from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from datashelf.core.config import get_config_tags_settings, validate_tags
from datashelf.core.hashing import sha256_hex
from typing import TypedDict, Optional
from tempfile import NamedTemporaryFile


class FileEntry(TypedDict):
    file_hash: str
    name: str
    stored_path: str  # relative to datashelf_path
    message: Optional[str]
    tag: Optional[str]
    datetime_added: str  # ISO 8601


class Metadata(TypedDict):
    schema_version: str
    last_modified: str  # ISO 8601
    files: list[FileEntry]


# =============================================================
# MAIN FUNCTIONS
# =============================================================
def init_metadata(datashelf_path: Path):
    """
    Initializes the basic datashelf metadata and then writes it to
    the datashelf_path as a file called 'metadata.json'.

    Args:
        datashelf_path (Path): Path to the .datashelf directory
    """
    metadata_path = str(datashelf_path / "metadata.json")
    config_path = datashelf_path / "config.yaml"
    config_hash = sha256_hex(data_path=config_path)

    metadata = {
        "schema_version": "1.0",
        "last_modified": _get_current_timestamp(),
        "files": [],
    }

    _atomic_write_json(path=Path(metadata_path), obj=metadata)


def create_file_entry(
    file_hash: str, name: str, stored_path: str, message: str, tag: str
):
    file_entry: FileEntry = {
        "file_hash": file_hash,
        "name": name,
        "stored_path": stored_path,
        "message": message,
        "tag": tag,
        "datetime_added": _get_current_timestamp(),
    }

    return file_entry


def load_metadata(datashelf_path: Path) -> dict:
    """
    Reads `metadata.json` from datashelf_path / 'metadata.json'
    and returns the document as a dictionary with keys:
        - schema_version: str
        - last_modified: str
        - files: list

    Args:
        datashelf_path (Path): Path to the .datashelf directory.

    Raises:
        FileNotFoundError: Raised if 'metadata.json' not found in
        datashelf_path
        ValueError: Raised if files key doesn't exist or if it doesn't
        contain a list

    Returns:
        dict: Dictionary containing content of 'metadata.json'
    """

    metadata_path = datashelf_path / "metadata.json"

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Unable to find metadata at {metadata_path}. Your `.datashelf/` directory may be corrupted. Consider reinitializing your DataShelf project."
        )

    metadata_json = _read_json(path=metadata_path)

    if "files" not in metadata_json or not isinstance(metadata_json["files"], list):
        msg = (
            "Invalid JOSN metadata. Your metadata file may be corrupted. "
            "Consider reinitializing your DataShelf project."
        )
        raise ValueError(msg)

    return metadata_json


# =============================================================
# HELPER FUNCTIONS
# =============================================================
def _get_current_timestamp() -> str:
    """
    Returns the current datetime in ISO 8601 format

    Returns:
        str: Current datetime
    """
    return datetime.now().replace(microsecond=0).isoformat()


def _atomic_write_text(path: Path, text: str) -> None:
    """
    Atomically writes the given text to a provided path.

    Args:
        path (Path): Path to write file to
        text (str): Text to pass into file
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with NamedTemporaryFile(
        "w", dir=str(path.parent), delete=False, encoding="utf-8"
    ) as tempfile:
        tempfile.write(text)
        tmp = Path(tempfile.name)

    tmp.replace(path)


def _atomic_write_json(path: Path, obj: dict) -> None:
    """
    Atomically write json using _atomic_write_text
    by applying json.dumps to text arg.

    Args:
        path (Path): Path to write file to
        obj (dict): JSON-type metadata (Python dict)
    """
    _atomic_write_text(path=path, text=json.dumps(obj, indent=4, ensure_ascii=False))


def _read_json(path: Path):
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)
