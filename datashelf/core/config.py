import yaml

def init_config(datashelf_path:Path):
    # Set up config file
    config:dict[str, dict[str, bool | list[str]]] = {}
    config["Config"] = {
        "Enforce CCDS Tags": True,
        "Allowed Tags": ["raw", "external", "intermediate", "processed"]
    }
    
    with open(datashelf_path/"config.yaml", "w") as config_file:
        yaml.safe_dump(config, config_file, sort_keys = False)