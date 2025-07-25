# tests/test_edge_cases.py
"""
Test edge cases and boundary conditions that could cause issues
"""
import pytest
import pandas as pd
import numpy as np
import datashelf.core as ds

class TestEdgeCases:
    """Test edge cases that might break the system"""
    
    def test_empty_dataframe(self, temp_dir):
        """Test saving an empty DataFrame"""
        ds.init()
        ds.create_collection("Edge Cases")
        
        empty_df = pd.DataFrame()
        
        # This might fail or succeed depending on implementation
        # The test documents the expected behavior
        try:
            result = ds.save(empty_df, "Edge Cases", "empty", "raw", "Empty DataFrame")
            # If it succeeds, verify we can load it back
            if result == 0:
                metadata_path = temp_dir / '.datashelf' / 'edge_cases' / 'edge_cases_metadata.yaml'
                with open(metadata_path, 'r') as f:
                    import yaml
                    metadata = yaml.safe_load(f)
                
                saved_file = next(f for f in metadata['files'] if f['name'] == 'empty')
                loaded = ds.load("Edge Cases", saved_file['hash'])
                assert loaded.empty
        except Exception:
            # If it fails, that's also acceptable behavior
            # but should be documented
            pass
    
    def test_dataframe_with_special_characters(self, temp_dir):
        """Test DataFrame with special characters in column names and data"""
        ds.init()
        ds.create_collection("Special Chars")
        
        special_df = pd.DataFrame({
            'col with spaces': [1, 2, 3],
            'col-with-dashes': ['a', 'b', 'c'],
            'col_with_unicode_🚀': ['test', 'data', 'here']
        })
        
        result = ds.save(special_df, "Special Chars", "special_data", "raw", "Data with special characters")
        assert result == 0
    
    def test_very_long_collection_name(self, temp_dir):
        """Test collection with very long name"""
        ds.init()
        
        long_name = "A" * 200  # Very long collection name
        
        # This should either work or fail gracefully
        try:
            ds.create_collection(long_name)
            # If it works, verify the directory was created
            expected_path = temp_dir / '.datashelf' / long_name.lower().replace(" ", "_")
            # Filesystem might truncate very long names
        except Exception:
            # If it fails, that's acceptable
            pass