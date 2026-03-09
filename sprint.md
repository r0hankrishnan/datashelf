# One week sprint to MVP

This document outlines some functionality goals in order to have a "showcase"-able MVP by the end of spring break.

Yes — and **DataShelf is probably even easier to make resume-worthy quickly** than Magpie.

Why? Because DataShelf maps much more directly to the kinds of things recruiters already recognize:

* data pipeline tooling
* reproducibility
* metadata/versioning
* developer tooling
* storage abstractions
* CLI/package design

That makes it especially strong for:

* **Data Science**
* **MLE**
* **AI Engineering**
* also somewhat **PM**, if you frame the user problem well

The trick is the same: **do not try to build the full long-term vision right now**. Build the smallest version that already feels like a real tool.

---

# The 1-Week Resume Goal for DataShelf

You want to be able to say:

> Built a Python package and CLI for lightweight dataset versioning and artifact tracking, enabling reproducible data workflows through metadata, hashing, and structured local storage.

That is already a strong resume line if the repo is clean and demoable.

---

# What the bare minimum should be

By the end of the week, the minimum credible version of DataShelf should do **4 things**:

1. **initialize a project**
2. **save datasets/artifacts with metadata**
3. **load/list saved artifacts**
4. **track versions using content hashes**

If it does those four things cleanly, you can list it.

---

# What the final demo should look like

In an interview or on GitHub, you want to be able to show:

```bash
datashelf init
datashelf save data/raw/customers.csv --name customers_raw
datashelf save data/processed/customers_clean.csv --name customers_clean
datashelf list
datashelf load customers_clean
```

And then explain:

* each saved artifact gets metadata
* content is hashed
* artifacts are registered in a local catalog
* the tool supports reproducible loading by name or hash

That is enough to sound like a serious project.

---

# The smallest credible architecture

Keep it tight and clean.

```text
datashelf/
├── pyproject.toml
├── README.md
├── src/
│   └── datashelf/
│       ├── __init__.py
│       ├── cli.py
│       ├── catalog.py
│       ├── hashing.py
│       ├── storage.py
│       ├── models.py
│       └── utils.py
├── tests/
│   ├── test_hashing.py
│   ├── test_catalog.py
│   └── test_cli.py
└── example_project/
```

That structure alone helps a lot. It signals you know how to build a real Python package.

---

# The 4 core features to build

## 1. `datashelf init`

This initializes a project directory.

For example, it creates:

```text
.datashelf/
    catalog.json
    objects/
```

or

```text
.datashelf/
    catalog.db
    objects/
```

For the 1-week version, use **JSON** unless you really want SQLite.

### What it should do

* detect current project root
* create `.datashelf/`
* create empty catalog
* maybe create config file

### Why this matters

This makes the tool feel real, like git/dvc-lite.

---

## 2. `datashelf save`

This is the most important command.

Example:

```bash
datashelf save data/raw/customers.csv --name customers_raw
```

### What it should do

* verify file exists
* compute file hash
* create artifact record
* copy artifact into `.datashelf/objects/<hash>...`
* save metadata into catalog

### Minimum metadata to track

* artifact name
* original path
* stored path
* content hash
* file type
* timestamp
* optional user tags

If you want to impress recruiters, also track:

* file size
* extension
* short description

### Why this matters

This is where the project becomes “artifact tracking” rather than just a wrapper around file copy.

---

## 3. `datashelf list`

Example:

```bash
datashelf list
```

### What it should show

A clean table or readable output like:

```text
NAME              TYPE   HASH        CREATED
customers_raw     csv    a81e3c2f    2026-03-06
customers_clean   csv    b912af10    2026-03-06
```

### Why this matters

This is the proof that the catalog system works.

---

## 4. `datashelf load`

Example:

```bash
datashelf load customers_clean
```

or

```bash
datashelf load --hash b912af10
```

### What it should do

* resolve artifact by name or hash
* return the stored path
* optionally print metadata
* maybe copy it back out later, but not required for MVP

### Why this matters

Without load/retrieval, versioning feels incomplete.

---

# The truly important technical ingredient: hashing

This is the heart of the project.

You need a clean file hashing module.

### Minimum

Use SHA-256 on file bytes.

### Why it matters

This gives you:

* deduplication
* reproducibility
* content-addressed storage
* version identity

That one concept makes the project much more impressive.

---

# The bare minimum data model

You want an `ArtifactRecord` that looks something like:

```python
from dataclasses import dataclass

@dataclass
class ArtifactRecord:
    name: str
    original_path: str
    stored_path: str
    hash: str
    file_type: str
    created_at: str
    size_bytes: int
```

Even if you later move to Pydantic, this is enough now.

---

# What makes DataShelf immediately resume-worthy

For this project, recruiters will care about:

## 1. It is packaged properly

Use:

* `pyproject.toml`
* `src/` layout
* console entry point for CLI

This matters a lot.

## 2. It solves a real engineering problem

Frame it as:

* lightweight data artifact tracking
* reproducibility in ML/data workflows
* simplified local dataset versioning

## 3. It has tests

Even just 3–5 tests is enough to elevate it.

At minimum test:

* hash generation
* save/register behavior
* load resolution

## 4. It has a clean README with demo GIF or commands

This may matter as much as the code for internships.

---

# What you do NOT need in week one

Do not build these yet:

* remote storage
* S3 integration
* parquet schema introspection
* Spark integration
* migration framework
* full experiment tracking
* huge metadata ontology
* lineage graph
* UI/dashboard
* authentication
* team collaboration

Those are exciting, but not needed to list it.

---

# The bare minimum resume bullet set

After a solid one-week build, you should be able to write something like:

**DataShelf — Lightweight Data Artifact Versioning Tool**

* Built a Python package and CLI for lightweight dataset versioning and artifact tracking in local ML/data workflows
* Implemented content-addressed storage using SHA-256 hashing to support reproducible retrieval and deduplication of saved artifacts
* Designed a metadata catalog for artifact registration, enabling listing and lookup by name or hash
* Structured the tool as a tested, installable Python package with modular storage, hashing, and CLI components

That is already very strong.

---

# What would make it stronger for different roles

## For Data Science internships

Add:

* notebook demo showing reproducible dataset loading
* maybe pandas integration helper like `datashelf.load_df("customers_clean")`

## For MLE / AI Engineering

Add:

* stronger package structure
* tests
* typed models
* clean CLI
* content-addressed storage explanation
* optional support for multiple file types

## For Product / PM internships

Add:

* README section explaining user problem:
  “data practitioners often lose track of dataset versions and transformations in ad hoc notebook workflows”

---

# The smallest “showable” GitHub repo

Your repo should include:

## README

Must have:

* what problem it solves
* quickstart
* architecture overview
* example commands
* future roadmap

## Example demo

Maybe an `example_project/` folder with:

* raw csv
* cleaned csv
* commands used

## Tests

At least a few

## CLI entry point

So a recruiter can see this is a real tool, not just scripts

---

# The actual threshold for “can I put this on my resume now?”

My honest bar would be:

You can list DataShelf as soon as all of these are true:

### Required

* `datashelf init` works
* `datashelf save` works
* `datashelf list` works
* `datashelf load` works
* hashes are used meaningfully
* repo is clean and structured
* README explains the project

### Strongly preferred

* at least 3 tests
* installable package via `pip install -e .`

If you hit that, it is fair game.

---

# What to prioritize if you only have one week

## Absolute priority order

1. package structure
2. hashing
3. save command
4. catalog
5. list/load commands
6. README
7. tests

If time remains:
8. pandas helper
9. nicer CLI output
10. version history per artifact name

---

# The best version of the 1-week scope

If I were scoping this aggressively, I would define the MVP as:

### Commands

* `datashelf init`
* `datashelf save <path> --name <name>`
* `datashelf list`
* `datashelf load <name-or-hash>`

### Internals

* local `.datashelf/objects/`
* catalog JSON
* SHA-256 hashing
* metadata records
* modular Python package

That’s it.

And honestly, that’s enough to start listing it.

---

# One subtle point: what story are you selling?

For interviews, do **not** pitch it as “poor man’s DVC.”

Pitch it as:

> I built a lightweight artifact-tracking tool for local data science workflows because I kept running into reproducibility and dataset-versioning friction in project work.

That sounds stronger, more original, and more user-driven.

---

# My bottom line

For **DataShelf**, the bare minimum to be resume-ready in one week is:

* an installable Python package
* CLI with `init/save/list/load`
* content hashing
* local artifact catalog
* clean README
* basic tests

That is enough to:

* demonstrate software engineering maturity
* show understanding of reproducibility/versioning
* talk about developer tooling design
* stand out from generic student ML projects

If you want, I can turn this into a **7-day execution plan for DataShelf**, with exact daily milestones and a “must finish / nice to have” split.
