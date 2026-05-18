from __future__ import annotations

import pandas as pd
import pytest

from pathlib import Path
from datashelf import load


def test_load_by_exact_name_returns_artifact_path(saved_artifact):
    entry = saved_artifact["entry"]
    datashelf_path = saved_artifact["datashelf_path"]

    resolved = load("people_raw")

    assert resolved == datashelf_path / entry["stored_path"]
    assert isinstance(resolved, Path)
    assert resolved.exists()


def test_load_by_hash_prefix_returns_artifact_path(saved_artifact):
    entry = saved_artifact["entry"]
    datashelf_path = saved_artifact["datashelf_path"]
    short_hash = entry["file_hash"][:8]

    resolved = load(short_hash)

    assert resolved == datashelf_path / entry["stored_path"]
    assert isinstance(resolved, Path)
    assert resolved.exists()


def test_load_to_df_returns_dataframe(saved_artifact):
    df = load("people_raw", to_df=True)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "name"]
    assert len(df) == 2


def test_load_missing_key_raises_value_error(saved_artifact):
    with pytest.raises(ValueError):
        load("does_not_exist")
