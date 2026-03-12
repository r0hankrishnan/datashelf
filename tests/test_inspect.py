from __future__ import annotations

from datashelf.inspect import ls, show


def test_ls_prints_saved_entry(saved_artifact, capsys):
    ls()
    captured = capsys.readouterr()

    assert "people_raw" in captured.out
    assert "raw" in captured.out
    assert "tiny test dataset" in captured.out


def test_ls_filter_tag_prints_matching_entries_only(saved_artifact, capsys):
    ls(filter_tag=["raw"])
    captured = capsys.readouterr()

    assert "people_raw" in captured.out
    assert "raw" in captured.out


def test_show_prints_full_metadata_entry(saved_artifact, capsys):
    show("people_raw")
    captured = capsys.readouterr()

    assert "Hash" in captured.out
    assert "Name" in captured.out
    assert "Tag" in captured.out
    assert "Stored at" in captured.out
    assert "people_raw" in captured.out
