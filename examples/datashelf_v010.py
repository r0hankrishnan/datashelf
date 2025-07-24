import marimo

__generated_with = "0.14.13"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # DataShelf Example

    This notebook demonstrates the core functionality of DataShelf - a git-like version control system for datasets.

    We'll walk through:
    1. Setting up a DataShelf project
    2. Creating collections to organize datasets
    3. Saving and versioning datasets
    4. Understanding the metadata structure

    *Thanks Claude for helping with the dialogue :)*
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Setup

    First, let's import the necessary libraries and create some sample data to work with.
    """
    )
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import datashelf.core as ds

    # Create sample datasets for our example
    np.random.seed(42)

    # Sample sales data
    sales_data = pd.DataFrame({
        'product': ['Widget A', 'Widget B', 'Widget C', 'Widget D'],
        'units_sold': [150, 200, 75, 300],
        'price': [25.99, 45.50, 15.00, 60.00],
        'region': ['North', 'South', 'East', 'West']
    })

    print("Sample sales data:")
    print(sales_data)
    return ds, pd, sales_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 1: Initialize DataShelf

    Before we can start versioning datasets, we need to initialize DataShelf in our project directory. This creates a `.datashelf` folder that will store all our metadata and dataset versions.
    """
    )
    return


@app.cell
def _(ds):
    # Note: This will prompt you to confirm the directory
    # In a real scenario, make sure you're in your project root
    ds.init()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 2: Create a Collection

    Collections help organize related datasets. Think of them like folders for your data versions. Let's create a collection for our sales analysis.
    """
    )
    return


@app.cell
def _(ds):
    # Create a collection for sales data
    ds.create_collection("Sales Analysis 2024")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 3: Save Dataset Versions

    Now we can start saving dataset versions. Each save includes:
    - **name**: A descriptive name for this dataset
    - **tag**: A label (like "raw", "cleaned", "final")
    - **message**: A commit message explaining what this version contains
    """
    )
    return


@app.cell
def _(ds, sales_data):
    # Save the raw sales data
    ds.save(df=sales_data, 
         collection_name="Sales Analysis 2024", 
         name="quarterly_sales", 
         tag="raw", 
         message="Initial quarterly sales data from database")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 4: Creating Data Transformations

    Let's create some transformed versions of our data and save them as new versions.
    """
    )
    return


@app.cell
def _(sales_data):
    # Add calculated columns
    sales_enriched = sales_data.copy()
    sales_enriched['revenue'] = sales_enriched['units_sold'] * sales_enriched['price']
    sales_enriched['revenue_per_unit'] = sales_enriched['revenue'] / sales_enriched['units_sold']

    print("Enriched sales data:")
    print(sales_enriched)
    return (sales_enriched,)


@app.cell
def _(ds, sales_enriched):
    # Save the enriched version
    ds.save(df=sales_enriched, 
         collection_name="Sales Analysis 2024", 
         name="quarterly_sales", 
         tag="enriched", 
         message="Added revenue calculations and per-unit metrics")
    return


@app.cell
def _(pd, sales_enriched):
    # Create a summary dataset
    sales_summary = pd.DataFrame({
        'total_units': [sales_enriched['units_sold'].sum()],
        'total_revenue': [sales_enriched['revenue'].sum()],
        'avg_price': [sales_enriched['price'].mean()],
        'top_product': [sales_enriched.loc[sales_enriched['revenue'].idxmax(), 'product']]
    })

    print("Sales summary:")
    print(sales_summary)
    return (sales_summary,)


@app.cell
def _(ds, sales_summary):
    # Save the summary
    ds.save(df=sales_summary, 
         collection_name="Sales Analysis 2024", 
         name="sales_summary", 
         tag="final", 
         message="Final summary statistics for quarterly report")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 5: Testing Duplicate Detection

    DataShelf automatically detects when you try to save identical data and prevents duplicates.
    """
    )
    return


@app.cell
def _(ds, sales_data):
    # Try to save the same data again
    ds.save(df=sales_data, 
         collection_name="Sales Analysis 2024", 
         name="duplicate_test", 
         tag="raw", 
         message="This should be detected as a duplicate")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Step 6: Working with Multiple Collections

    Let's create another collection to demonstrate organization.
    """
    )
    return


@app.cell
def _(ds, pd):
    # Create a second collection
    ds.create_collection("Customer Analytics")

    # Create some customer data
    customer_data = pd.DataFrame({
        'customer_id': range(1001, 1006),
        'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown'],
        'total_purchases': [5, 12, 3, 8, 15],
        'avg_order_value': [45.20, 67.80, 23.50, 55.10, 89.90]
    })

    print("Customer data:")
    print(customer_data)
    return (customer_data,)


@app.cell
def _(customer_data, ds):
    # Save to the customer analytics collection
    ds.save(df=customer_data, 
         collection_name="Customer Analytics", 
         name="customer_profiles", 
         tag="raw", 
         message="Initial customer profile data from CRM")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Understanding the DataShelf Structure

    Let's explore what DataShelf has created for us behind the scenes.
    """
    )
    return


@app.cell
def _():
    import os
    import yaml

    # Check the .datashelf directory structure
    def show_directory_tree(path, prefix="", max_depth=3, current_depth=0):
        if current_depth > max_depth:
            return

        items = sorted(os.listdir(path))
        for i, item in enumerate(items):
            item_path = os.path.join(path, item)
            is_last = i == len(items) - 1

            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item}")

            if os.path.isdir(item_path) and not item.startswith('.'):
                next_prefix = prefix + ("    " if is_last else "│   ")
                show_directory_tree(item_path, next_prefix, max_depth, current_depth + 1)

    print("DataShelf directory structure:")
    print(".datashelf/")
    show_directory_tree(".datashelf")
    return (yaml,)


@app.cell
def _(yaml):
    with open('.datashelf/datashelf_metadata.yaml', 'r') as _f:
        main_metadata = yaml.safe_load(_f)
    print('Main DataShelf metadata:')
    print(yaml.dump(main_metadata, default_flow_style=False, sort_keys=False))
    return


@app.cell
def _(yaml):
    with open('.datashelf/sales_analysis_2024/sales_analysis_2024_metadata.yaml', 'r') as _f:
        collection_metadata = yaml.safe_load(_f)
    print('Sales Analysis 2024 collection metadata:')
    print(yaml.dump(collection_metadata, default_flow_style=False, sort_keys=False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Summary

    In this example, we've demonstrated the current capabilities of DataShelf:

    **What DataShelf can do now:**
    - Initialize project-level dataset versioning
    - Create organized collections for related datasets
    - Save pandas DataFrames with metadata (tags, messages, timestamps)
    - Automatically detect and prevent duplicate data storage
    - Maintain comprehensive metadata about all dataset versions
    - Track dataset history with SHA-256 hashing

    **Coming in future versions:**
    - Load specific dataset versions by name/tag
    - Compare datasets across different time periods
    - Restore previous dataset states
    - Command-line interface
    - Support for additional data formats (Polars, etc.)

    DataShelf provides a solid foundation for dataset version control, making it easy to track how your data evolves throughout your analysis workflow.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
