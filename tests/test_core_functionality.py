# tests/test_core_functionality.py
"""
Test the main public API functions that users interact with.
This covers the core functionality without testing every internal helper.
"""
import pytest
import pandas as pd
import numpy as np
import yaml
from pathlib import Path
import datashelf.core as ds

class TestCoreWorkflow:
    """Test the main user workflow: init -> create_collection -> save -> load/checkout"""
    
    def test_full_workflow_with_csv_format(self, temp_dir, sample_dataframe):
        """Test complete workflow: init, create collection, save, load"""
        # 1. Initialize
        result = ds.init()
        assert result == 0
        assert (temp_dir / '.datashelf').exists()
        
        # 2. Create collection
        ds.create_collection("Test Collection")
        collection_path = temp_dir / '.datashelf' / 'test_collection'
        assert collection_path.exists()
        
        # 3. Save data
        result = ds.save(
            df=sample_dataframe,
            collection_name="Test Collection",
            name="test_data",
            tag="raw",
            message="Test dataset"
        )
        assert result == 0
        
        # 4. Verify file was created (CSV for small data)
        csv_files = list(collection_path.glob('*.csv'))
        assert len(csv_files) == 1
        
        # 5. Load data back and verify it's identical
        metadata_path = collection_path / 'test_collection_metadata.yaml'
        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)
        
        saved_file = next(f for f in metadata['files'] if f['name'] == 'test_data')
        loaded_df = ds.load("Test Collection", saved_file['hash'])
        
        pd.testing.assert_frame_equal(loaded_df, sample_dataframe)
    
    def test_large_data_uses_parquet(self, temp_dir, large_dataframe):
        """Test that large datasets automatically use Parquet format"""
        ds.init()
        ds.create_collection("Large Data")
        
        result = ds.save(
            df=large_dataframe,
            collection_name="Large Data",
            name="big_dataset",
            tag="raw",
            message="Large dataset test"
        )
        assert result == 0
        
        # Should create parquet file, not CSV
        collection_path = temp_dir / '.datashelf' / 'large_data'
        parquet_files = list(collection_path.glob('*.parquet'))
        csv_files = list(collection_path.glob('*.csv'))
        
        assert len(parquet_files) == 1
        assert len(csv_files) == 0  # No CSV files for large data
    
    def test_duplicate_detection_works(self, temp_dir, sample_dataframe):
        """Test that identical datasets are detected and not saved twice"""
        ds.init()
        ds.create_collection("Duplicate Test")
        
        # Save once
        result1 = ds.save(sample_dataframe, "Duplicate Test", "original", "raw", "First save")
        assert result1 == 0
        
        # Try to save identical data
        result2 = ds.save(sample_dataframe, "Duplicate Test", "duplicate", "raw", "Second save")
        assert result2 == 1  # Should detect duplicate
        
        # Verify only one data file was created
        collection_path = temp_dir / '.datashelf' / 'duplicate_test'
        data_files = list(collection_path.glob('original_raw.*'))
        assert len(data_files) == 1

class TestErrorHandling:
    """Test error conditions and edge cases"""
    
    def test_save_without_init_fails(self, temp_dir, sample_dataframe):
        """Test that saving without initializing fails gracefully"""
        with pytest.raises(Exception):  # Should fail somehow
            ds.save(sample_dataframe, "Test", "data", "raw", "message")
    
    def test_invalid_tag_rejected(self, temp_dir, sample_dataframe):
        """Test that invalid tags are rejected"""
        ds.init()
        ds.create_collection("Tag Test")
        
        with pytest.raises(ValueError, match="not a valid tag"):
            ds.save(sample_dataframe, "Tag Test", "data", "invalid_tag", "message")
    
    def test_all_valid_tags_accepted(self, temp_dir, sample_dataframe):
        """Test that all default valid tags work"""
        ds.init()
        ds.create_collection("Valid Tags")
        
        valid_tags = ['raw', 'intermediate', 'cleaned', 'ad-hoc', 'final']
        
        for i, tag in enumerate(valid_tags):
            # Modify data slightly to avoid duplicate detection
            df = sample_dataframe.copy()
            df['test_col'] = i
            
            result = ds.save(df, "Valid Tags", f"data_{tag}", tag, f"Test {tag}")
            assert result == 0
    
    def test_unsupported_data_type_rejected(self, temp_dir):
        """Test that non-DataFrame objects are rejected"""
        ds.init()
        ds.create_collection("Type Test")
        
        with pytest.raises(ValueError, match="Unsupported data type"):
            ds.save({"not": "a dataframe"}, "Type Test", "data", "raw", "message")

class TestMultipleCollections:
    """Test working with multiple collections"""
    
    def test_multiple_collections_independent(self, temp_dir, sample_dataframe):
        """Test that multiple collections work independently"""
        ds.init()
        
        # Create multiple collections
        ds.create_collection("Collection A")
        ds.create_collection("Collection B")
        
        # Save different data to each
        df_a = sample_dataframe.copy()
        df_b = sample_dataframe.copy()
        df_b['extra'] = 'B data'
        
        ds.save(df_a, "Collection A", "data_a", "raw", "Data for A")
        ds.save(df_b, "Collection B", "data_b", "raw", "Data for B")
        
        # Verify both collections have their own data
        assert (temp_dir / '.datashelf' / 'collection_a').exists()
        assert (temp_dir / '.datashelf' / 'collection_b').exists()
        
        # Verify metadata shows 2 collections
        metadata_path = temp_dir / '.datashelf' / 'datashelf_metadata.yaml'
        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)
        
        assert metadata['metadata']['number_of_collections'] == 2

class TestDisplayAndInspection:
    """Test metadata display functions"""
    
    def test_ls_functions_dont_crash(self, temp_dir, sample_dataframe):
        """Test that ls functions work without crashing (basic smoke test)"""
        ds.init()
        ds.create_collection("Display Test")
        ds.save(sample_dataframe, "Display Test", "data", "raw", "Test data")
        
        # These should not raise exceptions
        try:
            ds.ls("ds-md")
            ds.ls("ds-coll")
            # Note: coll-md and coll-files require user input, so skip in automated tests
        except SystemExit:
            # Some display functions might call input() which can cause issues in tests
            pass

class TestCheckoutAndLoad:
    """Test data retrieval functions"""
    
    def test_checkout_creates_file_in_working_directory(self, temp_dir, sample_dataframe):
        """Test that checkout creates a file in the working directory"""
        ds.init()
        ds.create_collection("Checkout Test")
        ds.save(sample_dataframe, "Checkout Test", "test_data", "raw", "Test")
        
        # Get hash from metadata
        metadata_path = temp_dir / '.datashelf' / 'checkout_test' / 'checkout_test_metadata.yaml'
        with open(metadata_path, 'r') as f:
            metadata = yaml.safe_load(f)
        
        saved_file = next(f for f in metadata['files'] if f['name'] == 'test_data')
        
        # Checkout should create file in working directory
        result = ds.checkout("Checkout Test", saved_file['hash'])
        assert result == 0
        
        # Should find the checked out file
        checkout_files = list(temp_dir.glob('test_data_raw.*'))
        assert len(checkout_files) == 1

class TestConfigurationBasics:
    """Test basic configuration functionality"""
    
    def test_tag_enforcement_enabled_by_default(self, temp_dir):
        """Test that tag enforcement is enabled by default"""
        ds.init()
        
        from datashelf.core.config import check_tag_enforcement, get_allowed_tags
        
        assert check_tag_enforcement() == True
        
        tags = get_allowed_tags()
        assert isinstance(tags, list)
        assert len(tags) > 0
        assert 'raw' in tags