# DataShelf   

A git-like version control system for datasets.

## Overview

DataShelf helps data scientists and analysts track how their datasets evolve over time. Similar to how git tracks code changes, DataShelf tracks dataset versions with metadata, tags, and commit messages.

## Key Features

- **Version Control for Data**: Track dataset changes with timestamps, tags, and descriptive messages
- **Hash-Based Deduplication**: Automatically detect and prevent duplicate dataset storage
- **Collection Organization**: Group related datasets into logical collections
- **Metadata Tracking**: Comprehensive logging of dataset history and modifications
- **Pandas Integration**: Native support for pandas DataFrames

## Core Concepts

- **Collections**: Logical groupings of related datasets (e.g., "Q4_sales_data", "user_analytics")
- **Versioning**: Each dataset save creates a timestamped version with metadata
- **Tags**: Label versions for easy identification (e.g., "raw", "cleaned", "final")
- **Messages**: Descriptive commit messages explaining dataset changes

## Quick Start

### Using the CLI
```bash
# Initialize datashelf in your project
datashelf init

# Or initialize in a specific directory
datashelf init --path /path/to/project

# Create a collection for your datasets
datashelf create-collection sales_analysis
```
### Using Python API

```python
import datashelf.core as ds
import pandas as pd

# Initialize datashelf in your project
ds.init()

# Create a collection for your datasets
ds.create_collection("sales_analysis")

# Save a dataset version
df = pd.DataFrame({"product": ["A", "B"], "sales": [100, 200]})
ds.save(df, 
     collection_name="sales_analysis", 
     name="raw_sales", 
     tag="raw", 
     message="Initial sales data import")
```

## Project Structure

```
your_project/
├── .datashelf/
│   ├── datashelf_metadata.yaml
│   └── collection_name/
│       ├── collection_metadata.yaml
│       └── dataset_files.csv
├── your_notebooks.ipynb
└── your_scripts.py
```

## Installation

### From Source

```bash
git clone https://github.com/yourusername/datashelf.git
cd datashelf
pip install -e .
```

### Direct from GitHub

```bash
pip install git+https://github.com/yourusername/datashelf.git
```

### Development Installation

For contributors or those wanting to modify the code:

```bash
git clone https://github.com/yourusername/datashelf.git
cd datashelf
pip install -e ".[dev]"
```

## Use Cases

### Current Capabilities
- **Dataset Versioning**: Save and track pandas DataFrames with timestamps, tags, and messages
- **Duplicate Prevention**: Automatically detect when you're trying to save identical data
- **Collection Organization**: Group related datasets into organized collections
- **Metadata Logging**: Maintain detailed records of all dataset changes and additions

### Future Capabilities (Work in Progress)
- **Experiment Tracking**: Load specific dataset versions for comparison and analysis
- **Reproducibility**: Restore previous dataset states from any point in history
- **Data Pipeline Management**: Compare datasets across different pipeline stages

## Contributing

This project is in early development. If you're interested in contributing or have feedback, please open an issue.

## Roadmap

The following are changes that are planned for the next release of DataShelf:

- [ ] Basic code improvements
     - [ ] Refactor core.py to make main functions simpler and pull out nested logic into helper functions
          - [x] init
          - [ ] create_collection
          - [ ] save
          - [ ] load
          - [ ] list

- [ ] Tagging system improvememnts
     - [ ] Implement default tag list with validation in save()
     - [ ] Allow tag default override
     - [ ] Update naming convention to combine name and tag

- [ ] Complete version management features
     - [ ] List all versions of a data set
          - [ ] Display in a nice table
     - [ ] Load a specific dataset
     - [ ] Create auto-versioning mechanic
     - [ ] Allow parent-child relationships

- [ ] Refactor metadata
     - [ ] Rename 'config' keys in YAML to 'metadata'
     - [ ] Ensure consistent metadata tracking for all DataShelf functions

- [ ] Update helper functions
     - [ ] Integrate into class-based design
     - [ ] Add more error handling

- [ ] Expand CLI integration
     - [ ] Add save, ls, and load to CLI commands
     - [ ] Allow for tag filtering in CLI
     - [ ] Update CLI styling

- [ ] Add a diff functionality to show simple comparisons between two datasets

- [ ] Support other data storage formats
     - [ ] Intelligently store data based on data size

- [ ] Build visualization helpers to show collection history and tag stats

- [ ] Refactor core entities into classes (if needed for more complex state management)
     - [ ] Datashelf class
     - [ ] Collection class
     - [ ] DatasetVersion class