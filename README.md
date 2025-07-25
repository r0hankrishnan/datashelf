# DataShelf   

![DataShelf logo and tagline](./assets/DataShelf-no-bg.svg)

A simple version control system for datasets.

## Overview

DataShelf helps data scientists and analysts track how their datasets evolve over time. Similar to how git tracks code changes, DataShelf tracks dataset versions with metadata, tags, and commit messages using an intuitive, git-inspired API.

## Key Features

- **Version Control for Data**: Track dataset changes with timestamps, tags, and descriptive messages
- **Hash-Based Deduplication**: Automatically detect and prevent duplicate dataset storage using SHA-256 hashing
- **Collection Organization**: Group related datasets into logical collections
- **Smart File Format Selection**: Automatically chooses optimal format (CSV/Parquet) based on data size
- **Comprehensive Metadata Tracking**: Detailed logging of dataset history and modifications
- **Data Retrieval**: Load any previous dataset version back into memory as pandas DataFrames
- **CLI Interface**: Command-line tools for common operations
- **Tag Enforcement**: Configurable validation to maintain consistent tagging standards

## Core Concepts

- **Collections**: Logical groupings of related datasets (e.g., "sales_analysis_q4", "customer_analytics")
- **Versioning**: Each dataset save creates a timestamped version with auto-incrementing version numbers
- **Tags**: Label versions for easy identification (e.g., "raw", "intermediate", "cleaned", "final", "ad-hoc")
- **Messages**: Descriptive commit messages explaining dataset changes
- **Hashes**: Unique SHA-256 identifiers for each dataset version enabling deduplication and retrieval

## Quick Start

### Using the Python API

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

# Load a previous version back into memory
loaded_df = ds.load("sales_analysis", "dataset_hash_here")

# View collection metadata
ds.ls("coll-files")  # Shows all datasets in a collection
```

### Using the CLI

```bash
# Initialize datashelf in your project
datashelf init

# Create a collection for your datasets
datashelf create-collection sales_analysis

# View project metadata
datashelf ls ds-md

# View all collections
datashelf ls ds-coll

# View collection files (interactive)
datashelf ls coll-files

# Checkout a dataset to working directory
datashelf checkout collection_name dataset_hash
```

## Project Structure

```
your_project/
├── .datashelf/
│   ├── datashelf_metadata.yaml      # Project-level metadata
│   ├── datashelf_config.yaml        # Configuration settings
│   └── collection_name/
│       ├── collection_metadata.yaml # Collection-specific metadata
│       └── dataset_files.[csv|parquet] # Your versioned datasets
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

## Core API Reference

### Initialization
- `ds.init()` - Initialize DataShelf in current directory
- `ds.create_collection(name)` - Create a new collection

### Data Operations  
- `ds.save(df, collection_name, name, tag, message)` - Save a dataset version
- `ds.load(collection_name, hash_value)` - Load dataset into pandas DataFrame
- `ds.checkout(collection_name, hash_value)` - Copy dataset file to working directory

### Metadata & Inspection
- `ds.ls("ds-md")` - Show DataShelf project metadata
- `ds.ls("ds-coll")` - Show all collections overview
- `ds.ls("coll-md")` - Show specific collection metadata
- `ds.ls("coll-files")` - Show all files in a collection

### Configuration
- `check_tag_enforcement()` - Check if tag validation is enabled
- `get_allowed_tags()` - Get list of valid tags
- `set_tag_enforcement(boolean)` - Enable/disable tag validation-- **Not recommended to use**

## Use Cases

### Current Capabilities (v0.2.0)
- **Dataset Versioning**: Save and track pandas DataFrames with comprehensive metadata
- **Data Retrieval**: Load any previous dataset version back into memory for analysis
- **Duplicate Prevention**: Automatically detect and prevent saving identical datasets
- **Collection Organization**: Group related datasets into organized, searchable collections  
- **Metadata Management**: Maintain detailed records of all dataset changes with timestamps and version numbers
- **CLI Operations**: Perform common tasks via command-line interface
- **Smart Storage**: Automatic CSV/Parquet format selection based on data size
- **Configuration Management**: Customizable tag enforcement and validation rules

### Future Capabilities (Planned)
- **Dataset Comparison**: Visual and statistical comparison between dataset versions
- **Branch-like Functionality**: Create divergent analysis paths from any dataset version
- **Advanced Query Interface**: Search and filter datasets by metadata
- **Integration Hooks**: Connect with popular ML frameworks and data pipelines
- **Collaboration Features**: Share and sync collections across team members

## Configuration

DataShelf includes configurable options for team consistency:

```python
# Check current settings
ds.check_tag_enforcement()  # Returns True/False
ds.get_allowed_tags()       # Returns ['raw', 'intermediate', 'cleaned', 'ad-hoc', 'final']

# Customize tag enforcement
ds.set_tag_enforcement(True)  # Enforce valid tags
```

Default configuration includes:
- **Tag enforcement**: Enabled by default
- **Allowed tags**: `['raw', 'intermediate', 'cleaned', 'ad-hoc', 'final']`
- **Auto-format selection**: CSV for <10MB, Parquet for ≥10MB

## Examples

Check out the comprehensive examples in the [`examples/`](./examples/) directory:

- [`datashelf_v020.ipynb`](./examples/v0.2.0/datashelf_v020.ipynb) - Full feature walkthrough

## Contributing

DataShelf is actively developed and welcomes contributions! Whether you're interested in:

- **Bug fixes** - Help us improve stability
- **New features** - Implement planned functionality  
- **Documentation** - Improve guides and examples
- **Testing** - Expand test coverage
- **Ideas** - Suggest new capabilities

Please open an issue or submit a pull request. For major changes, please open an issue first to discuss your ideas.

## Changelog

### v0.2.0 (Current)
- Full dataset loading with `ds.load()`
- File checkout with `ds.checkout()`  
- Comprehensive CLI interface
- Metadata display system with `ds.ls()`
- Default tag enforcement
- Smart file format selection
- Enhanced error handling and validation

### v0.1.0
- Basic dataset saving and versioning
- Collection management
- Hash-based deduplication
- Core metadata tracking