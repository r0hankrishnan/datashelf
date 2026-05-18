from __future__ import annotations

import json

from datashelf import init


def test_init_creates_datashelf_directory_and_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    init()

    datashelf_path = tmp_path / ".datashelf"
    assert datashelf_path.exists()
    assert datashelf_path.is_dir()

    config_path = datashelf_path / "config.yaml"
    metadata_path = datashelf_path / "metadata.json"

    assert config_path.exists()
    assert metadata_path.exists()

    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert "schema_version" in metadata
    assert "last_modified" in metadata
    assert "files" in metadata
    assert isinstance(metadata["files"], list)


def test_init_is_safe_to_run_twice(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    init()
    init()

    datashelf_path = tmp_path / ".datashelf"
    assert datashelf_path.exists()
    assert (datashelf_path / "config.yaml").exists()
    assert (datashelf_path / "metadata.json").exists()
