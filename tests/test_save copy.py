from __future__ import annotations

import json


def test_save_creates_artifact_and_metadata_entry(initialized_repo, sample_csv):
    from datashelf import save

    save(
        data=sample_csv,
        name="people_raw",
        message="tiny test dataset",
        tag="raw",
    )

    datashelf_path = initialized_repo / ".datashelf"
    metadata_path = datashelf_path / "metadata.json"

    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert len(metadata["files"]) == 1

    entry = metadata["files"][0]
    assert entry["name"] == "people_raw"
    assert entry["message"] == "tiny test dataset"
    assert entry["tag"] == "raw"
    assert entry["stored_path"].startswith("artifacts/")
    assert len(entry["file_hash"]) == 64

    artifact_path = datashelf_path / entry["stored_path"]
    assert artifact_path.exists()
    assert artifact_path.suffix == ".parquet"


def test_duplicate_save_with_same_tag_does_not_create_second_entry(
    initialized_repo, sample_csv
):
    from datashelf import save

    save(
        data=sample_csv,
        name="people_raw",
        message="tiny test dataset",
        tag="raw",
    )
    save(
        data=sample_csv,
        name="people_raw_again",
        message="same underlying data",
        tag="raw",
    )

    metadata_path = initialized_repo / ".datashelf" / "metadata.json"
    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = json.load(f)

    assert len(metadata["files"]) == 1
