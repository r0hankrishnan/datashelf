# DataShelf
```                                   
           _____          _           _____  _            _   __ 
          |  __ \        | |         / ____|| |          | | / _|
(\__/)    | |  | |  __ _ | |_  __ _ | (___  | |__    ___ | || |_
(•ㅅ•)     | |  | | / _` || __|/ _` | \___ \ | '_ \  / _ \| ||  _|
/ づ■づ    | |__| || (_| || |_| (_| | ____) || | | ||  __/| || |  
          |_____/  \__,_| \__|\__,_||_____/ |_| |_| \___||_||_|  
```
```                                                                                                                                                         
DDDDDDDDDDDDD                                 tttt                               SSSSSSSSSSSSSSS hhhhhhh                                lllllll    ffffffffffffffff  
D::::::::::::DDD                           ttt:::t                             SS:::::::::::::::Sh:::::h                                l:::::l   f::::::::::::::::f 
D:::::::::::::::DD                         t:::::t                            S:::::SSSSSS::::::Sh:::::h                                l:::::l  f::::::::::::::::::f
DDD:::::DDDDD:::::D                        t:::::t                            S:::::S     SSSSSSSh:::::h                                l:::::l  f::::::fffffff:::::f
  D:::::D    D:::::D  aaaaaaaaaaaaa  ttttttt:::::ttttttt      aaaaaaaaaaaaa   S:::::S             h::::h hhhhh           eeeeeeeeeeee    l::::l  f:::::f       ffffff
  D:::::D     D:::::D a::::::::::::a t:::::::::::::::::t      a::::::::::::a  S:::::S             h::::hh:::::hhh      ee::::::::::::ee  l::::l  f:::::f             
  D:::::D     D:::::D aaaaaaaaa:::::at:::::::::::::::::t      aaaaaaaaa:::::a  S::::SSSS          h::::::::::::::hh   e::::::eeeee:::::eel::::l f:::::::ffffff       
  D:::::D     D:::::D          a::::atttttt:::::::tttttt               a::::a   SS::::::SSSSS     h:::::::hhh::::::h e::::::e     e:::::el::::l f::::::::::::f       
  D:::::D     D:::::D   aaaaaaa:::::a      t:::::t              aaaaaaa:::::a     SSS::::::::SS   h::::::h   h::::::he:::::::eeeee::::::el::::l f::::::::::::f       
  D:::::D     D:::::D aa::::::::::::a      t:::::t            aa::::::::::::a        SSSSSS::::S  h:::::h     h:::::he:::::::::::::::::e l::::l f:::::::ffffff       
  D:::::D     D:::::Da::::aaaa::::::a      t:::::t           a::::aaaa::::::a             S:::::S h:::::h     h:::::he::::::eeeeeeeeeee  l::::l  f:::::f             
  D:::::D    D:::::Da::::a    a:::::a      t:::::t    tttttta::::a    a:::::a             S:::::S h:::::h     h:::::he:::::::e           l::::l  f:::::f             
DDD:::::DDDDD:::::D a::::a    a:::::a      t::::::tttt:::::ta::::a    a:::::a SSSSSSS     S:::::S h:::::h     h:::::he::::::::e         l::::::lf:::::::f            
D:::::::::::::::DD  a:::::aaaa::::::a      tt::::::::::::::ta:::::aaaa::::::a S::::::SSSSSS:::::S h:::::h     h:::::h e::::::::eeeeeeee l::::::lf:::::::f            
D::::::::::::DDD     a::::::::::aa:::a       tt:::::::::::tt a::::::::::aa:::aS:::::::::::::::SS  h:::::h     h:::::h  ee:::::::::::::e l::::::lf:::::::f            
DDDDDDDDDDDDD         aaaaaaaaaa  aaaa         ttttttttttt    aaaaaaaaaa  aaaa SSSSSSSSSSSSSSS    hhhhhhh     hhhhhhh    eeeeeeeeeeeeee llllllllfffffffff 
```
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
