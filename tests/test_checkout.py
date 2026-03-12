from __future__ import annotations

from datashelf import checkout


def test_checkout_copies_artifact_to_destination(saved_artifact):
    dest = saved_artifact["project_root"] / "exports" / "people_checked_out.parquet"

    result = checkout("people_raw", dest)

    assert result == dest.resolve()
    assert dest.exists()
    assert dest.suffix == ".parquet"
