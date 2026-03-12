import pandas as pd
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from datashelf.core.config import (
    get_config_tags_settings,
    validate_tags,
    get_parquet_engine,
)
from datashelf.core.directory import find_datashelf_path
from datashelf.core.hashing import sha256_hex, make_temp_parquet
from datashelf.core.metadata import (
    load_metadata,
    _atomic_write_json,
    create_file_entry,
    _get_current_timestamp,
)


def save(data: pd.DataFrame | str | Path, name: str, message: str, tag: str) -> None:
    """Save data to the datashelf.

    Args:
        data (pd.DataFrame | str | Path): The data to be saved. Can be a pandas DataFrame, a file path as a string, or a Path object.
        name (str): The name to assign to the saved data.
        message (str): A message describing the saved data.
        tag (str): The tag to associate with the saved data.
    """
    datashelf_path: Path = find_datashelf_path()

    tag_validation_enforced, allowed_tags = get_config_tags_settings(
        datashelf_path=datashelf_path
    )
    if tag_validation_enforced:
        validate_tags(tag=tag, allowed_tags=allowed_tags)

    # Open a temporary directory for hash validation and metadata update processes
    with TemporaryDirectory(dir=datashelf_path) as t_dir:
        temp_dir = Path(t_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_data_path = temp_dir / "data.parquet"

        engine = get_parquet_engine(datashelf_path=datashelf_path)
        make_temp_parquet(data=data, output_path=temp_data_path, engine=engine)
        data_hash = sha256_hex(data_path=temp_data_path)

        metadata = load_metadata(datashelf_path=datashelf_path)
        metadata_path = datashelf_path / "metadata.json"

        # Check if hash already exists in metadata["files"]
        for entry in metadata["files"]:
            if entry["file_hash"] == data_hash and entry["tag"] == tag:
                print(
                    f"Data {name} already exists in .datashelf with hash {entry['file_hash']}."
                )
                return

            elif entry["file_hash"] == data_hash and entry["tag"] != tag:
                msg = (
                    "This data already exists in .datashelf under a different tag with the following metadata:\n\n"
                    f"\t- Hash: {entry['file_hash'][:8] + '...'}\n\t- Name: {entry['name']}\n\t- Message: {entry['message']}"
                    f"\n\t- Tag: {entry['tag']}\n\n"
                    "Would you like to update the metadata of this entry with the following metadata? (Y/N)\n\n"
                    f"\t-New Name: {name}\n\t- New Message: {message}\n\t-New Tag: {tag}\n"
                )
                response = input(msg)

                valid_response = (
                    True if response.lower() in ["y", "n", "yes", "no"] else False
                )

                while not valid_response:
                    if not valid_response:
                        response = input("Invalid response. Please enter Y or N. ")
                        valid_response = (
                            True
                            if response.lower() in ["y", "n", "yes", "no"]
                            else False
                        )

                if response.lower() in ["y", "yes"]:
                    # Update
                    metadata["last_modified"] = _get_current_timestamp()
                    entry["name"] = name
                    entry["message"] = message
                    entry["tag"] = tag

                    _atomic_write_json(path=metadata_path, obj=metadata)

                    print(f"Updated metadata for existing artifact {data_hash[:8]}.")
                    return

                else:
                    print("No changes made.")
                    return

            else:
                continue

        artifacts_dir = datashelf_path / "artifacts"
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        full_stored_path = artifacts_dir / f"{data_hash}.parquet"
        stored_path = f"artifacts/{data_hash}.parquet"

        shutil.move(str(temp_data_path), str(full_stored_path))

        data_file_entry = create_file_entry(
            file_hash=data_hash,
            name=name,
            stored_path=stored_path,
            message=message,
            tag=tag,
        )
        metadata["last_modified"] = _get_current_timestamp()
        metadata["files"].append(data_file_entry)

        _atomic_write_json(path=metadata_path, obj=metadata)

    print(f"Successfully saved '{name}' with hash {data_hash[:8]}.")
