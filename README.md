# datashelf
Track versions of datasets as they evolve over time.

datashelf: Lightweight Dataset Versioning Tool
Goal: Track versions of datasets as they evolve over time — even across projects.

**Key Concepts:**
- Think of it like git for datasets (but simpler).
- Maintains a .datashelf/ log with:
- Hashes of data files (e.g., .csv, .parquet, .json)
- Metadata (date, tags, notes, file paths)
- Can integrate into pipelines to checkpoint datasets during analysis.
- Works with raw files or in-memory DataFrames.

**Core Use Cases:**
- “Save this intermediate dataset with a version label.”
- “Compare this data snapshot to one from two weeks ago.”
- “Restore a specific dataset version.”

**Focus:**
- Dataset history, reproducibility, versioning.
- Supports multiple formats, not just pandas.
