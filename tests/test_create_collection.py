import pytest
import datashelf.core as ds
from datashelf.utils import tools
from pathlib import Path
import yaml
import re

def test_create_collection(temp_dir, monkeypatch):
    # 1. Initialize
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = ds.init()
    assert result == 0
    assert (temp_dir / '.datashelf').exists()
    
    # 2. Create collection
    monkeypatch.setattr(
        tools,
        "_find_datashelf_root",
        lambda return_datashelf_path=True: temp_dir / ".datashelf"
    )
    result = ds.create_collection("Test Collection")
    collection_path = temp_dir / '.datashelf' / 'test_collection'
    assert result == 0
    assert collection_path.exists()
    
    
    # 3. Check metadata files
    assert (collection_path/'test_collection_metadata.yaml').exists()
    with open(temp_dir/'.datashelf'/'datashelf_metadata.yaml', 'r') as f:
        data = yaml.safe_load(f)
    collection_key = "test_collection"
    assert collection_key in data['metadata']['collections']
    assert any(collection.get("collection_name") == collection_key for collection in data["collections"])
    
def test_error_create_collection_without_datashelf(temp_dir, monkeypatch):
    # 1. Create collection without initializing .datashelf
    err_msg = ".datashelf does not exist. Please initialize datashelf with init() before creating a collection."
    with pytest.raises(NotADirectoryError):
        monkeypatch.setattr(
        tools,
        "_find_datashelf_root",
        lambda return_datashelf_path=True: temp_dir / ".datashelf"
        )
        ds.create_collection("Test Collection")

def test_error_find_collection_without_metadata(temp_dir, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _:"yes")
    result = ds.init()
    assert result == 0
    assert (temp_dir / '.datashelf').exists()
    
    monkeypatch.setattr(
        tools,
        "_find_datashelf_root",
        lambda return_datashelf_path=True: temp_dir / ".datashelf"
    )
    result = ds.create_collection("Test Collection")
    collection_path = temp_dir / '.datashelf' / 'test_collection'
    metadata_path = collection_path / 'test_collection_metadata.yaml'
    assert result == 0
    assert collection_path.exists()
    assert metadata_path.exists()
    
    metadata_path.unlink()
    
    err_msg = (
                f"Collection directory '{collection_path}' exists but the metadata file test_collection_metadata.yaml does not.\n"
                f"This may indicate a corrupted or manually modified state. Consider deleting and recreating the collection."
            )
    with pytest.raises(FileNotFoundError):
        ds.create_collection("Test Collection")
