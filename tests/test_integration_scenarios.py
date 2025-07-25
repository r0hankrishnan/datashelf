# tests/test_integration_scenarios.py
"""
Test realistic usage scenarios that might uncover integration issues
"""
import pytest
import pandas as pd
import numpy as np
import datashelf.core as ds

class TestRealWorldScenarios:
    """Test scenarios that mimic real-world usage"""
    
    def test_data_science_workflow(self, temp_dir):
        """Test a typical data science workflow"""
        # Setup
        ds.init()
        ds.create_collection("Customer Analysis")
        
        # 1. Raw data
        raw_data = pd.DataFrame({
            'customer_id': range(1, 101),
            'age': np.random.randint(18, 80, 100),
            'income': np.random.randint(20000, 150000, 100),
            'purchases': np.random.randint(0, 50, 100)
        })
        
        ds.save(raw_data, "Customer Analysis", "raw_customers", "raw", "Raw customer data from database")
        
        # 2. Cleaned data
        cleaned_data = raw_data.copy()
        cleaned_data = cleaned_data[cleaned_data['age'] >= 18]  # Remove invalid ages
        cleaned_data['income_bracket'] = pd.cut(cleaned_data['income'], 
                                              bins=[0, 30000, 60000, 100000, float('inf')], 
                                              labels=['Low', 'Medium', 'High', 'Premium'])
        
        ds.save(cleaned_data, "Customer Analysis", "cleaned_customers", "cleaned", "Cleaned and categorized customer data")
        
        # 3. Analytics
        summary = cleaned_data.groupby('income_bracket').agg({
            'purchases': ['mean', 'sum'],
            'customer_id': 'count'
        }).round(2)
        summary.columns = ['avg_purchases', 'total_purchases', 'customer_count']
        summary = summary.reset_index()
        
        ds.save(summary, "Customer Analysis", "customer_summary", "final", "Customer analysis by income bracket")
        
        # Verify we can load any version
        metadata_path = temp_dir / '.datashelf' / 'customer_analysis' / 'customer_analysis_metadata.yaml'
        with open(metadata_path, 'r') as f:
            import yaml
            metadata = yaml.safe_load(f)
        
        # Should have 4 files (metadata + 3 saved datasets)
        assert len(metadata['files']) == 4
        
        # Each saved dataset should be loadable
        data_files = [f for f in metadata['files'] if f['name'] != 'customer_analysis_metadata.yaml']
        assert len(data_files) == 3
        
        for file_info in data_files:
            loaded = ds.load("Customer Analysis", file_info['hash'])
            assert loaded is not None
            assert len(loaded) > 0
    
    def test_experiment_tracking(self, temp_dir):
        """Test using DataShelf for experiment tracking"""
        ds.init()
        ds.create_collection("ML Experiments")
        
        # Base dataset
        base_data = pd.DataFrame({
            'feature_1': np.random.randn(1000),
            'feature_2': np.random.randn(1000),
            'target': np.random.randint(0, 2, 1000)
        })
        
        ds.save(base_data, "ML Experiments", "base_features", "raw", "Base feature set")
        
        # Experiment 1: Add polynomial features
        exp1_data = base_data.copy()
        exp1_data['feature_1_squared'] = exp1_data['feature_1'] ** 2
        exp1_data['feature_interaction'] = exp1_data['feature_1'] * exp1_data['feature_2']
        
        ds.save(exp1_data, "ML Experiments", "poly_features", "ad-hoc", "Experiment 1: Polynomial features")
        
        # Experiment 2: Normalized features
        exp2_data = base_data.copy()
        exp2_data['feature_1'] = (exp2_data['feature_1'] - exp2_data['feature_1'].mean()) / exp2_data['feature_1'].std()
        exp2_data['feature_2'] = (exp2_data['feature_2'] - exp2_data['feature_2'].mean()) / exp2_data['feature_2'].std()
        
        ds.save(exp2_data, "ML Experiments", "normalized_features", "ad-hoc", "Experiment 2: Normalized features")
        
        # Verify all experiments are tracked
        metadata_path = temp_dir / '.datashelf' / 'ml_experiments' / 'ml_experiments_metadata.yaml'
        with open(metadata_path, 'r') as f:
            import yaml
            metadata = yaml.safe_load(f)
        
        experiment_files = [f for f in metadata['files'] if f['tag'] == 'ad-hoc']
        assert len(experiment_files) == 2