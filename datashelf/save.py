from tempfile import TemporaryDirectory
from typing import Literal
import shutil
from pathlib import Path

import pandas as pd

from datashelf.core.config import (
    get_config_tags_settings,
    validate_tags,
    get_parquet_engine,
)
from datashelf.core.directory import find_datashelf_path
from datashelf.core.hashing import sha256_hex, make_temp_parquet
from datashelf.core.metadata import (
    Metadata,
    load_metadata,
    update_metadata,
    create_file_entry,
    get_current_timestamp,
)


# Define Error class for when on_duplicate = "error"
class DuplicateError(Exception):
    pass


# =============================================================
# MAIN FUNCTION
# =============================================================
def save(
    data: pd.DataFrame | str | Path,
    name: str,
    message: str,
    tag: str,
    on_duplicate: Literal["skip", "error", "update"] = "skip",
) -> None:
    """Save data to the datashelf.

    Args:
        data (pd.DataFrame | str | Path): The data to be saved. Can be a pandas DataFrame, a file path as a string, or a Path object.
        name (str): The name to assign to the saved data.
        message (str): A message describing the saved data.
        tag (str): The tag to associate with the saved data.
        on_duplicate (Literal['skip', 'error', 'update']): Whether to
        skip, error, or update when a duplicate is found. Defaults to skip.
    """
    datashelf_path: Path = find_datashelf_path()

    _validate_tag(datashelf_path=datashelf_path, tag=tag)

    # Open a temporary directory for hash validation and metadata update processes
    with TemporaryDirectory(dir=datashelf_path) as t_dir:
        temp_data_path, data_hash = _hash_data(
            temp_dir=t_dir, datashelf_path=datashelf_path, data=data
        )

        metadata: Metadata = load_metadata(datashelf_path=datashelf_path)
        metadata_path = datashelf_path / "metadata.json"

        duplicate_handled = _handle_duplicate(
            metadata=metadata,
            metadata_path=metadata_path,
            data_hash=data_hash,
            name=name,
            message=message,
            tag=tag,
            on_duplicate=on_duplicate,
        )

        # duplicate_handled = True means that the helper dealt with a duplicate file and we don't need to write anything
        if duplicate_handled:
            return

        stored_path = _store_artifact(
            datashelf_path=datashelf_path,
            temp_data_path=temp_data_path,
            data_hash=data_hash,
        )
        data_file_entry = create_file_entry(
            file_hash=data_hash,
            name=name,
            stored_path=stored_path,
            message=message,
            tag=tag,
        )
        metadata["last_modified"] = get_current_timestamp()
        metadata["files"].append(data_file_entry)

        update_metadata(path=metadata_path, obj=metadata)


# =============================================================
# HELPER FUNCTIONS
# =============================================================
def _validate_tag(datashelf_path: Path, tag: str):
    """Reads config file to see if tag validation is on.
    If so, validates proposed tag and if tag is not in
    allowed_tag, throws an error.

    Args:
        datashelf_path (Path): Path to .datashelf/
        tag (str): User inputted tag for data they are trying to save.

    Raises:
        ValueError: Propogated from validate_tag() if tag not in allowed_tags.
    """
    tag_validation_enforced, allowed_tags = get_config_tags_settings(
        datashelf_path=datashelf_path
    )
    if tag_validation_enforced:
        validate_tags(
            tag=tag, allowed_tags=allowed_tags
        )  # Raises ValueError if validation fails


def _hash_data(
    temp_dir: Path | str, datashelf_path: Path, data: pd.DataFrame | str | Path
) -> tuple[Path, str]:
    """Meant to run within TemporaryDirectory context manager.
    Creates the temporary directory, creates the path for the
    normalized temporary parquet file, and hashes the temporary parquet file.

    Args:
        temp_dir (Path | str): Path to temporary directory.
        datashelf_path (Path): Path to .datashelf/
        data (pd.DataFrame): Data user is trying to save (passed to save()).

    Returns:
        tuple[Path, str]: Tuple containing the temporary data file's path and the hash of the data file.
    """
    temp_dir = Path(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_data_path = temp_dir / "data.parquet"

    engine = get_parquet_engine(datashelf_path=datashelf_path)
    make_temp_parquet(data=data, output_path=temp_data_path, engine=engine)
    data_hash = sha256_hex(data_path=temp_data_path)

    return temp_data_path, data_hash


def _store_artifact(datashelf_path: Path, temp_data_path: Path, data_hash: str) -> str:
    """Stores the parquet file of the data being saved into an artifacts/ directory
    in .datashelf/ by moving the parquet file from its temporary directory to
    the artifact directory.

    Args:
        datashelf_path (Path): The path to .datashelf/
        temp_data_path (Path): The path to the temporary directory.
        data_hash (str): The data's hash string.

    Returns:
        str: The path (relative to .datahself/) where the .parquet artifact is stored.
    """
    artifacts_dir = datashelf_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    full_stored_path = artifacts_dir / f"{data_hash}.parquet"
    stored_path = f"artifacts/{data_hash}.parquet"

    shutil.move(str(temp_data_path), str(full_stored_path))

    return stored_path


def _handle_duplicate(
    metadata: Metadata,
    metadata_path: Path,
    data_hash: str,
    name: str,
    message: str,
    tag: str,
    on_duplicate: Literal["skip", "error", "update"],
) -> bool:
    """Handles logic for if a duplicate file already exists in metadata. Depending on value
    of on_duplicate, the function either skips, errors out, or updates the duplicate file in
    the metadata.

    Args:
        metadata (Metadata): Metadata object.
        metadata_path (Path): Path to metadata json file in .datashelf/
        data_hash (str): Hash of data that user is trying to save
        name (str): Name of data that user is trying to save
        message (str): Message assigned to data that user is trying to save
        tag (str): Tag assigned to data that user is trying to save
        on_duplicate (Literal['skip', 'error', 'update']): Whether to
        skip, error, or update when a duplicate is found.

    Raises:
        DuplicateError: Error raised if on_duplicate = 'error'. Explains what the current entry's metadata is
        and prompts to rerun with either 'skip' or 'update'.

    Returns:
        bool: True is a duplicate was updated (this means we don't need to store/move artifacts), False if no
        duplicates were found (this means we need to store/move artifacts)
    """
    for entry in metadata["files"]:
        if entry["file_hash"] == data_hash:
            # This means that the data already exists in the metadata
            match on_duplicate:
                case "skip":
                    return True

                case "error":
                    err_msg = (
                        f"Data {name} already exists in .datashelf under "
                        f"name: {entry['name']} with hash: {entry['file_hash']} and tag: {entry['tag']}"
                        "\nIf you want to replace the existing file's metadata with the information you passed to save(), "
                        "call save() with on_duplicate set to 'update'."
                    )
                    raise DuplicateError(err_msg)

                case "update":
                    now = get_current_timestamp()
                    metadata["last_modified"] = now
                    entry["name"] = name
                    entry["message"] = message
                    entry["tag"] = tag
                    entry["datetime_modified"] = now

                    update_metadata(path=metadata_path, obj=metadata)

                    return True

    return False
