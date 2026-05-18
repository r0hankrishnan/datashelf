from pathlib import Path
from datashelf.core.metadata import init_metadata
from datashelf.core.directory import init_datashelf_directory
from datashelf.core.config import init_config


def init(custom_path: str | None = None) -> tuple[bool, Path]:
    """Initialize a datashelf directory. Recommended to initialize the datashelf at the root of your project.

    Args:
        custom_path (str | None, optional): The path to initialize the datashelf directory. If not provided, the datashelf directory will be initialized in the current working directory. Defaults to None.

    Raises:
        NotADirectoryError: If the specified path does not exist or is not a directory.
        
    Returns:
        bool: True if new .datashelf directory was created, False if .datashelf directory already existed at datashelf_path.
        Path: The path at which datashelf was intialized.
    """
    if custom_path:
        if not Path(custom_path).exists():
            raise NotADirectoryError(
                f"Could not find {custom_path}. Please enter an existing path within your project."
            )

        datashelf_path: Path = Path(custom_path) / ".datashelf"
        initialized = init_datashelf_directory(datashelf_path = datashelf_path)

        if initialized: # Initialize .datashelf at datashelf_path
            init_config(datashelf_path=datashelf_path)
            init_metadata(datashelf_path=datashelf_path)
        
        return initialized, datashelf_path

    else:
        cwd: Path = Path().cwd()
        datashelf_path: Path = cwd / ".datashelf"
        initialized = init_datashelf_directory(datashelf_path = datashelf_path)

        if initialized: # Initialize .datashelf at datashelf_path
            init_config(datashelf_path=datashelf_path)
            init_metadata(datashelf_path=datashelf_path)
        
        return initialized, datashelf_path
