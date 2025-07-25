## Python Implementation

You can use DataShelf in python. To get started import datashelf:

```python
import datashelf.core as ds
import pandas as pd
```

After importing datashelf, initialize your datashelf. When initializing your datashelf, make sure you are in your project's root directory (this will allow the metadata updating functions to easily find .datashelf/).

```python
ds.init()
```

Before saving any data, you need to create a collection. We recommend creating collections based on specific analyses.

```python
ds.create_collection("Sales Analysis Q4")
```

```python
sales_data = pd.DataFrame({
    'product_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
    'product_name': ['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Widget E'],
    'category': ['Electronics', 'Home', 'Electronics', 'Sports', 'Home'],
    'units_sold': [150, 200, 75, 300, 120],
    'unit_price': [25.99, 45.50, 15.00, 60.00, 35.75],
    'region': ['North', 'South', 'East', 'West', 'North']
})
```

```python
ds.save(
    df = sales_data,
    collection_name = "Sales Analysis Q4",
    name = "Quarterly Sales",
    tag = "raw",
    message = "Initial Q4  sales data from database export"
)
```

```python
sales_enriched = sales_data.copy()
sales_enriched['total_revenue'] = sales_enriched['units_sold'] * sales_enriched['unit_price']
sales_enriched['revenue_per_unit'] = sales_enriched['total_revenue'] / sales_enriched['units_sold']
sales_enriched['price_category'] = pd.cut(
    sales_enriched['unit_price'], 
    bins=[0, 30, 50, 100], 
    labels=['Low', 'Medium', 'High']
)
```

```python
# Save the enriched version
ds.save(
    df=sales_enriched,
    collection_name="Sales Analysis Q4",
    name="quarterly_sales",
    tag="intermediate",
    message="Added revenue calculations and price categorization"
)
```

```python
# Customer data - secondary dataset
customer_data = pd.DataFrame({
    'customer_id': range(1001, 1011),
    'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown',
             'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Ivy Chen', 'Jack Robinson'],
    'age': [28, 34, 22, 45, 31, 29, 38, 52, 26, 41],
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
             'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
    'total_purchases': [5, 12, 3, 8, 15, 7, 9, 4, 11, 6],
    'avg_order_value': [45.20, 67.80, 23.50, 55.10, 89.90, 38.75, 72.30, 41.60, 58.40, 49.20]
})
```

```python
ds.create_collection("Customer Analytics")
```

```python
ds.save(
    df=customer_data,
    collection_name="Customer Analytics",
    name="customer_profiles",
    tag="raw",
    message="Customer profile data from CRM system"
)
```

```
ds.ls("coll-files")
```

+---------------------------------+------------------------------------------------------------------+---------------------+----------------------+--------------+-----------+-----------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------+
| name                            | hash                                                             | date_created        | date_last_modified   | tag          |   version | message                                             | file_path                                                                                                                     | deleted   |
+=================================+==================================================================+=====================+======================+==============+===========+=====================================================+===============================================================================================================================+===========+
| sales_analysis_q4_metadata.yaml |                                                                  | 2025-07-25 09:52:34 |                      |              |           |                                                     | /Users/rohankrishnan/Documents/GitHub/datashelf/examples/v0.2.0/.datashelf/sales_analysis_q4/sales_analysis_q4_metadata.yaml  | False     |
+---------------------------------+------------------------------------------------------------------+---------------------+----------------------+--------------+-----------+-----------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------+
| Quarterly Sales                 | 9d77eabf6b934ce8e759742429021d0afeb2ccaa339c2db35ea4c96fdf96ff3f | 2025-07-25 09:52:42 | 2025-07-25 09:52:42  | raw          |         1 | Initial Q4  sales data from database export         | /Users/rohankrishnan/Documents/GitHub/datashelf/examples/v0.2.0/.datashelf/sales_analysis_q4/quarterly_sales_raw.csv          | False     |
+---------------------------------+------------------------------------------------------------------+---------------------+----------------------+--------------+-----------+-----------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------+
| quarterly_sales                 | 3976e38c4a19642f63ba16bb786b1eefe40313040e2e907830a4dc4205d12a10 | 2025-07-25 09:52:47 | 2025-07-25 09:52:47  | intermediate |         2 | Added revenue calculations and price categorization | /Users/rohankrishnan/Documents/GitHub/datashelf/examples/v0.2.0/.datashelf/sales_analysis_q4/quarterly_sales_intermediate.csv | False     |
+---------------------------------+------------------------------------------------------------------+---------------------+----------------------+--------------+-----------+-----------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------+
| category_summary                | 887054aa634c5fc4fc6b4c9e097f29d69d252902c42099832d8497a85aae333f | 2025-07-25 09:52:52 | 2025-07-25 09:52:52  | final        |         3 | Final category-level summary for Q4 report          | /Users/rohankrishnan/Documents/GitHub/datashelf/examples/v0.2.0/.datashelf/sales_analysis_q4/category_summary_final.csv       | False     |
+---------------------------------+------------------------------------------------------------------+---------------------+----------------------+--------------+-----------+-----------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------+

```
df = ds.load("Sales Analysis Q4", "9d77eabf6b934ce8e759742429021d0afeb2ccaa339c2db35ea4c96fdf96ff3f")
```