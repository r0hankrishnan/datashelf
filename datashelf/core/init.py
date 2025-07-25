from pathlib import Path
from datashelf.utils.logging import setup_logger
from datashelf.core.config import _initialize_datashelf_config
from datashelf.core.metadata import _initialize_datashelf_metadata

logger = setup_logger(__name__)

def init(set_dir:str = None):
    """_summary_

    Args:
        set_dir (str, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
        
    # If user sets a specific path for .datashelf
    if set_dir:
        msg = "set_dir functionality has not been fully built out for datashelf yet. Please run init() while in the desired directory for now."
        logger.error(msg)
        raise ValueError(msg)
        _init_with_set_dir(set_dir = set_dir)
    
    # If no set path, initialize .datashelf in cwd
    else:
        _init_with_current_dir()
        
def _init_with_set_dir(set_dir:str):
    
    set_dir = Path(set_dir)
    current_dir = Path.cwd()
    target_dir_path = set_dir.resolve()
    
    # Check if target_dir is subdirectory of current_dir
    try:
        target_dir_path.relative_to(current_dir)
        raise ValueError(
            f"Cannot initialize datashelf in a subdirectory ({target_dir_path}). "
            f"Datashelf should be initialized at or above the current directory "
            f"to ensure it can be found from all project files. "
            f"Consider running init() without set_dir, or use a parent directory."
        )
    except ValueError:
        pass
    
    # Create Path objects for datashelf dir and metadata file
    datashelf_path = target_dir_path / '.datashelf'
    metadata_file = datashelf_path / 'datashelf_metadata.yaml'
    
    if datashelf_path.is_dir() and metadata_file.exists():
        logger.info(".datashelf directory with metadata and config files already initialized")
        return 1
    else:
        datashelf_path.mkdir(parents=True, exist_ok=True)
        
        try:
            _initialize_datashelf_structure(set_dir = set_dir)
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        
        logger.info(".datashelf directory with config and metadata files initialized.")
        return 0

def _init_with_current_dir():

    # Warning message about running init() in the right directory
    while True:
        warning_msg = (
            "It is recommended that you init datashelf in your project's root directory. "
            "Datashelf may break if you create it in a subdirectory. "
            "Please check that you are in the project's root directory before continuing.\n"
            "Continue (y/n)?"
            )
        cont = input(warning_msg)
        if cont.lower().strip() in ["yes", "y"]:
            break
        elif cont.lower().strip() in ["no", "n"]:
            return None

    # Check current directory for .datashelf and create if DNE
    datashelf_path = Path.cwd()/'.datashelf'
    datashelf_metadata_path = datashelf_path/'datashelf_metadata.yaml'
    
    if datashelf_path.is_dir() and datashelf_metadata_path.exists():
        logger.info(".datashelf directory and metadata file already initialized.")
        return 1
    else:
        datashelf_path.mkdir(parents=True, exist_ok=True)
        
        try:
            _initialize_datashelf_structure()
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        
        logger.info(".datashelf directory with config and metadata files initialized.")
        return 0

def _initialize_datashelf_structure(set_dir:str = None):
    _initialize_datashelf_metadata(set_dir = set_dir)
    _initialize_datashelf_config(set_dir = set_dir)