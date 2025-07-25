# tests/conftest.py
import pytest
import pandas as pd
import numpy as np
import tempfile
import shutil
from pathlib import Path
import os

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_path = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    os.chdir(temp_path)
    yield Path(temp_path)
    os.chdir(original_cwd)
    shutil.rmtree(temp_path)

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
        'id': range(50000),
        'value': np.random.randn(50000),
        'category': np.random.choice(['X', 'Y', 'Z'], 50000)
    })





