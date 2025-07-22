# DataShelf   
(\__/)

(•ㅅ•)

/ づ■づ

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

```python
from datashelf.core import init, create_collection, save
import pandas as pd

# Initialize datashelf in your project
init()

# Create a collection for your datasets
create_collection("sales_analysis")

# Save a dataset version
df = pd.DataFrame({"product": ["A", "B"], "sales": [100, 200]})
save(df, 
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
