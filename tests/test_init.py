import pytest
import datashelf.core as ds
import tempfile
from pathlib import Path
import re


def test_init_creates_dot_datashelf(temp_dir, monkeypatch):
    # 1. Initialize
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    result = ds.init()
    assert result == 0
    assert (temp_dir / ".datashelf").exists()


def test_flagged_return_for_double_init(temp_dir, monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda _: "yes")
    ds.init()
    result_2 = ds.init()

    assert ".datashelf directory and metadata file already initialized." in caplog.text
    assert result_2 == 1


def test_set_dir_unimplemented_error():
    err_msg = "set_dir functionality has not been fully built out for datashelf yet. Please run init() while in the desired directory for now."
    with tempfile.TemporaryDirectory() as tempdir:
        set_dir = Path(tempdir)
        with pytest.raises(ValueError, match=re.escape(err_msg)):
            ds.init(set_dir=set_dir)
