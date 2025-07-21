# datashelf
Track versions of datasets as they evolve over time.

**Key Concepts:**
- Simple git-like tool for datasets.
- Maintains a .datashelf/ log with:
  - Hashes of data files
  - Metadata (date, tags, notes, file paths)
  - Works with raw files or in-memory DataFrames. *WIP*

**Core Use Cases:**
- “Save this intermediate dataset with a version label.”
- “Compare this data snapshot to one from two weeks ago.”
- “Restore a specific dataset version.”

**Focus:**
- Dataset history, reproducibility, versioning.
