import shutil
from pathlib import Path
from datashelf.load import load


def checkout(lookup_key: str, dest_path: str | Path) -> Path:
    """Copy a stored artifact from the datashelf to a user-specified destination.

    Args:
        lookup_key (str): Dataset name, full hash, or unique hash prefix.
        dest_path (str | Path): Destination file path to copy the artifact to.
    Raises:
        TypeError: If the destination file does not have a .parquet suffix.
        FileExistsError: If the destination file already exists.

    Returns:
        Path: The path to the copied artifact.
    """
    src_path = load(lookup_key = lookup_key)

    dest_path = Path(dest_path).resolve()

    if dest_path.suffix != ".parquet":
        raise TypeError(f"{dest_path} is invalid. Make sure file has .parquet suffix.")

    if dest_path.exists():
        raise FileExistsError(f"File already exists at: {dest_path}")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src_path), str(dest_path))

    return dest_path
