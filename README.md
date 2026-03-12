# Datashelf

![datashelf logo](./assets/datashelf.svg)

Datashelf is a lightweight **local dataset tracking tool** for data science projects.

It stores tabular datasets as immutable artifacts, tracks metadata, and lets you retrieve them later by **name or hash**. The goal is to make experiments easier to reproduce without introducing heavy infrastructure.

## Example

```bash
$ datashelf init
Initialized DataShelf at .datashelf/

$ datashelf save data/people.csv people_raw --message "tiny dataset" --tag raw
Successfully saved 'people_raw' with hash c8a2f8e1

$ datashelf list

Hash      Name         Tag   Message
-----------------------------------------
c8a2f8e1  people_raw   raw   tiny dataset
```

# Why Datashelf?

Many data science workflows struggle with dataset organization:

* intermediate datasets get overwritten
* multiple versions accumulate
* experiments become difficult to reproduce

Instead of accumulating files like:

```
data.csv
data_clean.csv
data_final_v2.csv
data_final_really_final.csv
```

Datashelf stores datasets using **content hashes** and maintains a metadata registry so artifacts can always be located again.

Key ideas:

* **content-addressed storage** (SHA256)
* **metadata registry** for datasets
* lookup by **name or hash prefix**
* **CLI + Python API**
* **opinionated dataset tags** based on Cookiecutter Data Science

It is intentionally **local and lightweight**, designed for individual projects rather than large data pipelines.

# Features

* Local dataset artifact storage
* SHA256 content hashing
* Metadata registry (name, tag, message, timestamp)
* Lookup by dataset name or hash prefix
* Optional dataset tags and messages
* CLI + Python API
* Automatic normalization to Parquet
* Duplicate dataset detection
* Basic unit test coverage


# Installation

Clone the repository and install locally:

```bash
git clone <repo-url>
cd datashelf
pip install -e .
```

I am also working on getting it published on PyPi!

# Quick Start

Initialize a Datashelf repository in your project directory:

```bash
datashelf init
```

This creates a hidden directory used to store artifacts and metadata:

```
.datashelf/
├── config.yaml
├── metadata.json
└── artifacts/
```

# Example Workflow

Save a dataset:

```bash
datashelf save data/people.csv people_raw --message "tiny dataset" --tag raw
```

List stored datasets:

```bash
datashelf list
```

Inspect metadata:

```bash
datashelf show people_raw
```

Load the stored dataset path:

```bash
datashelf load people_raw
```

Load directly into pandas:

```bash
datashelf load people_raw --df
```

Export the artifact to another location:

```bash
datashelf checkout people_raw exports/people.parquet
```

# Python API

Datashelf can also be used directly from Python:

```python
import datashelf as ds

ds.init()

ds.save(
    data="data.csv",
    name="training_data",
    message="clean dataset",
    tag="processed"
)

df = ds.load("training_data", to_df=True)
```

# Architecture

Datashelf separates **user commands** from **internal system services**.

```
User / CLI
    │
    ▼
Command Layer
(init, save, load, inspect, checkout)
    │
    ▼
Core Services
(directory, hashing, metadata, config)
    │
    ▼
.datashelf/
    artifacts + metadata registry
```

### Command Layer

Handles user workflows such as saving, loading, inspecting, and exporting datasets.

### Core Layer

Implements internal functionality including:

* content hashing
* metadata management
* artifact storage
* configuration management

This separation keeps command modules simple and makes core logic easier to test and maintain.

# How Artifacts Are Stored

Datasets are stored using their **SHA256 hash**:

```
.datashelf/artifacts/<hash>.parquet
```

Metadata is stored in a registry:

```json
{
  "file_hash": "c8a2f8e1...",
  "name": "people_raw",
  "tag": "raw",
  "message": "tiny dataset",
  "stored_path": "artifacts/c8a2f8e1.parquet",
  "datetime_added": "2026-03-10T12:30:00"
}
```

This ensures datasets can always be referenced reliably.

# Comparison

Datashelf focuses on **simple, local dataset tracking**.

| Tool      | Purpose                                             |
| --------- | --------------------------------------------------- |
| DataShelf | Lightweight local dataset tracking for tabular data |
| DVC       | Full data version control with remote storage       |
| Git LFS   | Large file versioning inside Git                    |

Datashelf intentionally avoids:

* Git integration
* remote storage
* pipeline orchestration

This keeps the tool simple and easy to use for smaller data science projects.

# Running Tests

Run tests with:

```bash
pytest
```

Tests cover repository initialization, dataset saving, loading, metadata inspection, and artifact checkout.

# Future Work

Possible extensions include:

* dataset diffing
* experiment tracking
* dataset lineage tracking
* remote artifact storage
* richer filtering and search

# License

MIT License.

# About This Project

Datashelf was built as a personal project to **make something that I thought would be useful in my day-to-day work at school**.

The project demonstrates:

* CLI tool development
* artifact-based dataset management
* modular Python package architecture
* reproducible data pipelines
* test-driven development


