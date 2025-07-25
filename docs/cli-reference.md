# DataShelf CLI Reference

This guide covers the available commands in the `datashelf` command-line interface.

## Initialization

```
datashelf init
```

Initializes DataShelf in the current directory.

## Collection Management

```
datashelf create-collection "Collection Name"
```

Creates a new collection. Names should be descriptive and unique.

## Metadata Inspection

```
datashelf ls ds-md
```

Displays project-level metadata.

```
datashelf ls ds-coll
```

Lists all existing collections.

```
datashelf ls coll-md
```

Displays metadata for a specific collection (interactive).

```
datashelf ls coll-files
```

Lists datasets stored in a collection (interactive).

## Data Retrieval

```
datashelf checkout <collection_name> <hash>
```

Exports a specific version of a dataset to your working directory.

---
