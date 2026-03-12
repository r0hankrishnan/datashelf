import yaml
from pathlib import Path
from typing import Literal

Tags = list[str]
Config = dict[str, dict[str, bool | Tags | str]]

def init_config(datashelf_path:Path):
    config: Config = {}
    
    config["config"] = {
        "enforce_ccds_tags": True,
        "allowed_tags": ["raw", "external", "intermediate", "processed"],
        "parquet_engine": "fastparquet"
    }
    
    with open(datashelf_path/"config.yaml", "w") as config_file:
        yaml.safe_dump(config, config_file, sort_keys = False)
        
def get_config_tags_settings(datashelf_path:Path) -> tuple[bool, list]:
    with open(datashelf_path / "config.yaml", "r") as config_file:
        content = yaml.safe_load(config_file)
        
    config = content["config"]
    
    if config["enforce_ccds_tags"]:
        return True, config["allowed_tags"]
    else:
        return False, []
    
def validate_tags(tag:str, allowed_tags:list[str]):
    if tag in allowed_tags:
        pass
    else:
        raise ValueError(f"Tag must be one of {', '.join(allowed_tags)}")
    
def get_parquet_engine(datashelf_path: Path) -> Literal["pyarrow", "fastparquet"]:
    with open(datashelf_path / "config.yaml", "r") as config_file:
        content = yaml.safe_load(config_file)
        
    config = content["config"]
    
    if config["parquet_engine"] not in ["pyarrow", "fastparquet"]:
        msg = (
            f"{config['parquet_engine']} is an invalid value for 'parquet_engine' in config.yaml file. "
            "Please change to either 'pyarrow' or 'fastparquet'"
        )
        raise ValueError(msg)
    
    return config["parquet_engine"]