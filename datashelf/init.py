from pathlib import Path
from datashelf.core.metadata import init_metadata
from datashelf.core.directory import init_datashelf_directory
from datashelf.core.config import init_config


def init(custom_path: str | None = None):
    """Initialize a datashelf directory. Recommended to initialize the datashelf at the root of your project.

    Args:
        custom_path (str | None, optional): The path to initialize the datashelf directory. If not provided, the datashelf directory will be initialized in the current working directory. Defaults to None.

    Raises:
        NotADirectoryError: If the specified path does not exist or is not a directory.
    """
    if custom_path:
        if not Path(custom_path).exists():
            raise NotADirectoryError(
                f"Could not find {custom_path}. Please enter an existing path within your project."
            )

        datashelf_path: Path = Path(custom_path) / ".datashelf"

        if init_datashelf_directory(datashelf_path=datashelf_path):
            print(f"Initialized DataShelf at {str(datashelf_path)}")
            init_config(datashelf_path=datashelf_path)
            init_metadata(datashelf_path=datashelf_path)

    else:
        cwd: Path = Path().cwd()
        datashelf_path: Path = cwd / ".datashelf"

        if init_datashelf_directory(datashelf_path=datashelf_path):
            print(f"Initialized DataShelf at {str(datashelf_path)}")
            init_config(datashelf_path=datashelf_path)
            init_metadata(datashelf_path=datashelf_path)
