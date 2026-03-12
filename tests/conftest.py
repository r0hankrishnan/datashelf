from __future__ import annotations

import json
from pathlib import Path

import pytest

from datashelf import init, save


@pytest.fixture
def initialized_repo(tmp_path, monkeypatch):
    """
    Create a temporary project directory, chdir into it, and initialize
    a DataShelf repository there.
    """
    monkeypatch.chdir(tmp_path)
    init()
    return tmp_path


@pytest.fixture
def sample_csv(initialized_repo: Path) -> Path:
    csv_path = initialized_repo / "people.csv"
    csv_path.write_text("id,name\n1,Alice\n2,Bob\n", encoding="utf-8")
    return csv_path


@pytest.fixture
def saved_artifact(initialized_repo: Path, sample_csv: Path):
    save(
        data=sample_csv,
        name="people_raw",
        message="tiny test dataset",
        tag="raw",
    )

    metadata_path = initialized_repo / ".datashelf" / "metadata.json"
    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    entry = metadata["files"][0]
    return {
        "project_root": initialized_repo,
        "datashelf_path": initialized_repo / ".datashelf",
        "csv_path": sample_csv,
        "metadata": metadata,
        "entry": entry,
    }
