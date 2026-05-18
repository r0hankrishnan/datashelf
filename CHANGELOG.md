# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Changelog was created at the start of v0.2.0, previous entries are reconstructed from best memory and in a way that logically flows. 

---

## [Unreleased]

### Added
- Delete functions: `delete_dataset()`, `delete_collection()`, `delete_shelf()`
- Save a CSV file directly by path without loading into a DataFrame first
- Parent-child relationships via `derived_from` parameter on `save()`
- Dataset diff: schema, row count, and summary statistic comparisons between two artifacts

### Changed
- Extracted shared name/hash lookup logic into `core/lookup.py`
- Exposed `write_metadata()` as a proper public function in `core/metadata.py`; `_atomic_write_json` remains private
- Dropped underscore from `get_current_timestamp()` to reflect its cross-module use
- Rich-formatted CLI output replacing plain `print()` calls
- Tag filtering available via `--filter-tag` flag on `datashelf list`

### Fixed
- Removed unused `config_hash` computation in `core/metadata.py`
- Renamed test files (`test_init copy.py`, etc.) so pytest picks them up correctly

---

## [0.1.2] — TBD

### Added
- `show` command: detailed per-entry metadata display via name or hash prefix
- `filter_tag` parameter on `ls()` for filtering displayed entries by tag
- Hash prefix matching in `load()`, `show()`, and `checkout()`

### Changed
- Improved error messages across `load()`, `show()`, and `checkout()` with actionable guidance

---

## [0.1.1] — TBD

### Added
- CLI support for `init`, `save`, `load`, `list`, `show`, and `checkout` commands
- `--df` flag on `datashelf load` to return artifact as a pandas DataFrame
- `--path` flag on `datashelf init` for custom initialization directory
- `--filter_tag` flag on `datashelf list`

### Changed
- Atomic writes via `NamedTemporaryFile` to prevent metadata corruption on failure

---

## [0.1.0] — TBD

### Added
- Initial release of core versioning functionality
- Python API: `init()`, `save()`, `load()`, `ls()`, `show()`, `checkout()`
- SHA256 content-addressed artifact storage under `.datashelf/artifacts/`
- Parquet normalization for canonical cross-format comparison
- Duplicate detection: same hash + same tag skips write; same hash + different tag prompts user
- `metadata.json` registry with schema version, last modified timestamp, and per-file entries
- `config.yaml` with tag enforcement (`enforce_ccds_tags`) and parquet engine selection
- Support for `.csv`, `.parquet`, `.xlsx`, and `.json` input formats
- Test suite with `conftest.py` fixtures for initialized repo, sample CSV, and saved artifact