# Advanced Usage

This guide walks through more advanced features of DataShelf, assuming you've already read [getting-started.md](./getting-started.md).

## Customizing Tags with `datashelf_config.yaml`

You can customize the tags used across all your datasets by editing `.datashelf/datashelf_config.yaml`. For example:

```yaml
config:
  default_tags:
    - raw
    - intermediate
    - final
```

## Working with Multiple Collections

You can manage multiple collections within a single DataShelf project. For example:

```python
import datashelf.core as ds

# Create multiple collections
collections = ["Sales Q1", "Sales Q2", "Customer Feedback"]
for coll in collections:
    ds.create_collection(coll)
```

To list all available collections:

```python
ds.ls("ds-coll")
```

To list .datashelf's metadata:

```python
ds.ls("ds-md")
```

This will show the date that the .datashelf directory was created, the number of collections in .datashelf/, and the names of each collection in .datashelf/.

### Philosophy: Organizing by Analysis

Collections should be used to group datasets that support the same analysis or purpose. This keeps your versioning clean, your saves intentional, and your work reproducible.

Examples:

Sales Analysis Q4: Raw exports, cleaned files, and model inputs used for Q4 sales forecasting

People Analytics Q4: Survey data, HR records, and cleaned features for employee churn analysis

Avoid mixing unrelated datasets in a single collection. Treat each collection like a self-contained story of your data exploration or modeling process.

## Viewing Collection Metadata

To inspect metadata for files in a collection, use:

```python
# Display collection file metadata in a formatted table
# (uses tabulate under the hood via display.py)
ds.ls(to_display="coll-files")
```

This will show version history, tags, messages, hashes, and file paths for each saved file.

You can also view the folder-level metadata of a collection by using:

```python
ds.ls(to_display = "coll-md")
```

This will show the collection name, the date the collection was created, the number of files in the collection, the most recent commit, and the max versioned data set in the collection.

## Resetting the Workspace

You can remove your current `.datashelf/` directory and reinitialize it:

```bash
rm -rf .datashelf/
```

```python
ds.init()
```

Note: This will **delete all version history**, so use cautiously.

## Tips for Scaling & Collaboration

* Use meaningful tags (`raw`, `joined`, `cleaned`, `model_input`, etc.)
* Add detailed commit messages when saving
* Use hashes instead of file names for guaranteed reproducibility
* Store `.datashelf/` in your repo's root directory
* Consider writing helper scripts that wrap `save()` with consistent naming/tag rules

---

For more on troubleshooting or CLI usage, see:

* [CLI Reference](./cli-reference.md)
* [Troubleshooting Guide](./troubleshooting.md)