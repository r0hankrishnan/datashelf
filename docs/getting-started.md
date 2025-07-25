# Getting Started with DataShelf

Welcome to **DataShelf**, a lightweight tool for dataset versioning. This guide will help you get started in less than five minutes.

---

## Quickstart (Python)

Install DataShelf:

```bash
pip install datashelf
```

Import and initialize in your project root:

```python
import datashelf.core as ds
import pandas as pd

ds.init()
```

Create a collection:

```python
ds.create_collection("Sales Analysis Q4")
```

Save your first dataset:

```python
sales_data = pd.DataFrame({
    'product_id': ['P001', 'P002'],
    'units_sold': [150, 200],
    'unit_price': [25.99, 45.50]
})

ds.save(
    df=sales_data,
    collection_name="Sales Analysis Q4",
    name="Quarterly Sales",
    tag="raw",
    message="Initial sales data"
)
```

Load a version by hash:

```python
df = ds.load("Sales Analysis Q4", "<snapshot-hash>")
```

Or check it out into your working directory:

```python
ds.checkout("Sales Analysis Q4", "<snapshot-hash>")
```

---

## What’s Next?

* [CLI Reference](./cli-reference.md): Use DataShelf from the command line
* [Troubleshooting](./troubleshooting.md): Fix common setup issues

For advanced features and usage patterns, see the future [Advanced Usage](./advanced-usage.md) guide.
