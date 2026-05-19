from __future__ import annotations

import pytest
from datashelf.inspect import ls, show


def test_ls_returns_saved_entry(saved_artifact):
    entries = ls()
    assert len(entries) == 1
    assert entries[0]["name"] == "people_raw"
    assert entries[0]["tag"] == "raw"
    assert entries[0]["message"] == "tiny test dataset"


def test_ls_returns_empty_list_when_no_entries(initialized_repo):
    entries = ls()
    assert entries == []


def test_ls_filter_tag_returns_matching_entries_only(saved_artifact):
    entries = ls(filter_tag=["raw"])
    assert len(entries) == 1
    assert entries[0]["tag"] == "raw"


def test_ls_filter_tag_returns_empty_for_no_matches(saved_artifact):
    entries = ls(filter_tag=["processed"])
    assert entries == []


def test_show_returns_matching_entry(saved_artifact):
    entries = show("people_raw")
    assert len(entries) == 1
    assert entries[0]["name"] == "people_raw"
    assert entries[0]["tag"] == "raw"


def test_show_raises_for_missing_key(saved_artifact):
    with pytest.raises(ValueError):
        show("does_not_exist")