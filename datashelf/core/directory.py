from pathlib import Path


def init_datashelf_directory(datashelf_path: Path) -> bool:
    """
    Checks if .datashelf already exists at datashelf_path and creates
    .datashelf directory if it doesn't

    Args:
        datashelf_path (Path): Path to check.
    """
    # Check if datashelf already exists at path -> else make .datashelf/ directory
    if datashelf_path.exists():  # should this raise an exception?
        print(f"Datashelf already initialized at {str(datashelf_path)}")
        return False

    else:
        datashelf_path.mkdir()
        return True


def find_datashelf_path() -> Path:
    """
    Walk up from current working directory and check for a
    .datashelf directory.

    Returns:
        Path | None: Path of .datashelf directory or None
    """
    curr_path = Path().cwd()

    while curr_path != curr_path.parent:
        if (curr_path / ".datashelf").exists():
            return curr_path / ".datashelf"
        else:
            curr_path = curr_path.parent

    msg = (
        "No Datashelf repository found. "
        "Datashelf searches upward from the current directory for a '.datashelf' folder.\n\n"
        "Searched upwards from:\n"
        f"{curr_path}\n\n"
        "If it exists in a subdirectory (e.g. data/.datashelf), run this command there."
    )

    raise FileNotFoundError(msg)
