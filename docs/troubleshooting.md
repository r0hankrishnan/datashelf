# DataShelf Troubleshooting Guide

This guide helps resolve common issues users may encounter.

## Initialization Errors

**Error**: `.datashelf` not found

**Solution**: Run `ds.init()` or `datashelf init` to initialize the project.

## Tag Validation Failures

**Error**: Invalid tag used when saving

**Solution**: Run `get_allowed_tags()` or inspect `datashelf_config.yaml`. Use only allowed tags like `raw`, `intermediate`, `cleaned`, `ad-hoc`, `final`.

## Collection Already Exists

**Error**: Collection name already in use

**Solution**: Use a different collection name. Collections are persistent and not overwritten.

## Dataset Not Found or Invalid Hash

**Error**: Cannot load or checkout dataset

**Solution**: Ensure you're using a valid SHA-256 hash from collection metadata. Use `ds.ls("coll-files")` to inspect available versions.

## Large Dataset Performance

**Issue**: Slow read/write for large datasets

**Solution**: DataShelf automatically uses Parquet for datasets ≥10MB for performance. Ensure required dependencies are installed.

---

For further help, file an issue on [GitHub](https://github.com/r0hankrishnan/datashelf/issues).