# Contributing to Datashelf

Thanks for your interest in Datashelf! This is a personal project I built to solve a real problem in my own data science workflow, and I'm happy to have others use it or contribute.

## Reporting Issues

If something isn't working, please open a GitHub issue. Include:

- What you ran
- What you expected to happen
- What actually happened
- Your Python version and OS

## Suggesting Features

Open an issue with the label `enhancement`. The [roadmap in the README](./README.md#roadmap) lists directions I'm already considering — feel free to weigh in there too.

## Pull Requests

1. Fork the repo and create a branch from `main`
2. Make your changes
3. Run the test suite: `pytest`
4. Open a pull request with a clear description of what you changed and why

Please keep PRs focused — one change per PR makes review much easier.

## Architecture Notes

Datashelf separates user-facing commands from internal services:

```
User / CLI
    │
    ▼
Command Layer       ← init, save, load, inspect, checkout
    │
    ▼
Core Services       ← hashing, metadata, storage, config
    │
    ▼
.datashelf/         ← artifacts/ + metadata.json
```

**Command modules** handle user workflows. They should stay thin — delegate to core services rather than implementing logic directly.

**Core modules** implement the underlying functionality (SHA256 hashing, Parquet normalization, metadata registry, etc.) and are where the unit tests live.

If you're adding a new command, the pattern is: add a CLI entry point, implement the workflow in the command layer, and add or extend a core service if new internal logic is needed.

## Contact

Feel free to reach out directly at [krishnan.rohan@outlook.com](mailto:krishnan.rohan@outlook.com) — especially if you're working on something interesting in data science.

Thank you for taking the time to interact with my project :)
