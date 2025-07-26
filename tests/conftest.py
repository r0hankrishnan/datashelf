# tests/conftest.py
import pytest
import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
import os

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            yield Path(tmpdir)
        finally:
            os.chdir(original_cwd)

@pytest.fixture
def sample_dataframe():
    """Create a sample pandas DataFrame for testing"""
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(1, 6),
        'name': [f'Item_{i}' for i in range(1, 6)],
        'value': [10.5, 20.3, 15.7, 8.9, 12.1],
        'category': ['A', 'B', 'A', 'C', 'B']
    })

@pytest.fixture
def large_dataframe():
    """Create a large DataFrame to test Parquet formatting"""
    np.random.seed(42)
    return pd.DataFrame({
        'id': range(200000),
        'value': np.random.randn(200000),
        'category': np.random.choice(['X', 'Y', 'Z'], 200000)
    })





