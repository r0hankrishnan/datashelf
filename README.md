# DataShelf

![DataShelf logo and tagline](./assets/DataShelf-no-bg.svg)

DataShelf is a lightweight version control system for datasets.

It helps analysts and data scientists manage evolving versions of their data—right from Python or the command line—without needing to track CSVs or Parquet files manually. It’s a useful tool for iterative workflows involving EDA, feature engineering, or model development.

## Key Features

- Track changes to datasets across time using hashes, tags, and messages
- Restore any prior version of a dataset, even after overwrites
- Group datasets into named collections for clean project structure
- Use simple CLI and Python commands to inspect, save, or retrieve files
- Avoid duplication, overwrite mistakes, or unclear file names

## Quick Example

```python
import datashelf.core as ds
import pandas as pd

ds.init()  # Creates .datashelf/ in your working directory

df_q4_sales = pd.DataFrame({
    "date": pd.date_range("2024-10-01", periods=10, freq="7D"),
    "product": np.random.choice(["Laptop", "Phone", "Tablet"], 10),
    "units_sold": np.random.randint(1, 20, 10),
    "unit_price": np.random.randint(300, 1500, 10)
})
df_q4_sales["total_sales"] = df_q4_sales["units_sold"] * df_q4_sales["unit_price"]

ds.save(df=df_q4_sales, collection_name="Sales Q4", name="Migrated Sales Q4 Data", tag="raw", message="Initial export")

# Checkout a prior version
ds.checkout(collection_name="Sales Q4", hash="abc123")
````

Or via CLI:

```bash
# Init and create collection
datashelf init
datashelf create_collection "Sales Q4"

# Save a file
datashelf save <file_path>

# Display collection files in a table
datashelf ls coll-files

# Checkout data
datashelf checkout <collection_name> <hash>
```

## Concepts

* **Collections**: Logical groups of datasets, usually tied to a single analysis or project
* **Tags**: Labels like `raw`, `cleaned`, `final` that describe dataset state
* **Messages**: Optional commit-style messages saved alongside each version
* **Hashes**: Unique identifiers used to retrieve exact versions
* **Snapshots**: Project-wide point-in-time saves of all collections

For example, you might have separate collections for:

* `Sales Forecasting Q4`
* `People Analytics Q4`
* `Customer Feedback Analysis`

Each collection tracks its own datasets independently.

## Installation

```bash
pip install datashelf
```

Requires Python 3.9+


## Documentation

* [Getting Started (5 min)](docs/getting-started.md)
* [CLI Reference](docs/cli-reference.md)
* [Troubleshooting](docs/troubleshooting.md)
* [Advanced Usage](docs/advanced-usage.md)

## Contributing

Issues, suggestions, and PRs welcome. If you'd like to get involved or have feedback, open an issue or submit a pull request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.


