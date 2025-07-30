# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project tries to adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add text wrapping to tabulate display
- Internal improvements and documentation refinements in preparation for v0.3.0
- Allow users to delete a data set from their collection
- Create a function to delete a collection
- Create a function to delete .datashelf/
- Move shelf.py and collection.py helper functions into .py file in core/
- Allow parent-child relationships
- Allow for tag filtering in CLI
- Update CLI styling
- Add a diff functionality to show simple comparisons between two datasets
- Build visualization helpers to show collection history and tag stats
- Allow users to save a csv file directly

## [v0.3.0] - 

## Added
- CLI function to save files to datashelf

## Changed
- Refactored ls table display to use rich library instead of tabulate
- Replaced stock ls function with separate multiselect ls function for CLI interface


## [v0.2.0] – 2025-07-24

### Added
- Introduced collection support to group datasets by analysis
- Added tagging system with optional tag color config in `datashelf_config.yaml`
- CLI support for `save`, `init`, and `ls` commands
- `display.py` module for tabulated views of saved files and metadata
- Support for snapshots and tracked file views via `ls(to_display=...)`
- Ability to manually specify checkout paths with `output_path` param

### Changed
- Refactored internal functions for improved separation of concerns
- Improved Python API ergonomics (fewer required params, better defaults)


## [v0.1.0] – 2025-07-12

### Added
- Initial release of core versioning functionality
- Basic Python API: `init()`, `save()`, `checkout()`, `ls()`
- Automatic hash tracking and metadata storage in `.datashelf/`
- Markdown-based metadata structure with YAML support
