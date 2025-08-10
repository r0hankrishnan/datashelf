import yaml
from pathlib import Path
from typing import List
from datashelf.utils.tools import _find_datashelf_root


def _initialize_datashelf_config(set_dir: str = None):
    """Creates a YAML file with basic config setup.

    Args:
        set_dir (str, optional): [Not currently implemented but eventually allow users to set a directory for .datashelf?]. Defaults to None.

    Returns:
        int: 0 if pass else throws an error
    """
    # Manually set path if set_dir is not None
    if set_dir:
        datashelf_path = Path(set_dir).resolve() / ".datashelf"
        datashelf_config_path = datashelf_path / "datashelf_config.yaml"
    else:
        datashelf_path = _find_datashelf_root(return_datashelf_path=True)
        datashelf_config_path = datashelf_path / "datashelf_config.yaml"

    # Create config structure
    config = {}

    config["tag_enforcement"] = True
    config["allowed_tags"] = ["raw", "intermediate", "cleaned", "ad-hoc", "final"]
    config["collection_tag_overrides"] = {}

    # Write to config file path
    with open(datashelf_config_path, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    return 0


def check_tag_enforcement() -> bool:
    """Checks if tags are enforced

    Returns:
        bool: TRUE if yes else FALSE
    """

    datashelf_path = _find_datashelf_root(return_datashelf_path=True)
    datashelf_config_path = datashelf_path / "datashelf_config.yaml"

    with open(datashelf_config_path, "r") as f:
        data = yaml.safe_load(f)

    return data["tag_enforcement"]


def set_tag_enforcement(tag_enforced: bool = True):
    """Function to toggle tag enforcement on or off.

    Args:
        tag_enforced (bool, optional): Whether to enforce set tags. Defaults to True.

    Raises:
        ValueError: Raised if tag_enforced is not a boolean but is "True" or "False"
        ValueError: Raised otherwise

    Returns:
        int: 0 if successful else throws an error
    """
    if not isinstance(tag_enforced, bool):
        if isinstance(tag_enforced, str) and tag_enforced.lower().strip() in [
            "true",
            "false",
        ]:
            raise ValueError(
                f'"{tag_enforced}" not valid. Write True or False instead. The arg must be a boolean.'
            )
        raise ValueError(
            f"tag_enforced arg must be either True or False. {tag_enforced} is not a valid input."
        )

    datashelf_path = _find_datashelf_root(return_datashelf_path=True)
    datashelf_config_path = datashelf_path / "datashelf_config.yaml"

    with open(datashelf_config_path, "r") as f:
        data = yaml.safe_load(f)

    data["tag_enforcement"] = tag_enforced

    with open(datashelf_config_path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    return 0


def get_allowed_tags() -> List[str]:
    """Get the list of allowed tags in the config file.

    Returns:
        List[str]: List of strings of the allowed tags.
    """

    datashelf_path = _find_datashelf_root(return_datashelf_path=True)
    datashelf_config_path = datashelf_path / "datashelf_config.yaml"
    with open(datashelf_config_path, "r") as f:
        data = yaml.safe_load(f)

    return data["allowed_tags"]
