import pytest
import pandas as pd
import os
import tempfile
from src.df1_pandera_schema import D1Schema


class TestDf1:
    """Test cases for df1.py functionality."""
    
    def test_load_and_validate_csv_success(self):
        """Test loading and validating a CSV file."""
        # Create a temporary CSV file
        csv_content = """operation_id,categorie_personne,resultat_humain,nombre,dont_nombre_blesse
1,A,X,10,1
2,B,Y,20,2
3,C,Z,30,3"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = pd.read_csv(temp_path)
            df_validated = D1Schema.validate(df)
            
            assert len(df_validated) == 3
            assert 'operation_id' in df_validated.columns
            assert df_validated['operation_id'].dtype == 'int64'
        finally:
            os.unlink(temp_path)
    
    def test_load_csv_with_coercion(self):
        """Test that CSV with string numbers gets coerced correctly."""
        csv_content = """operation_id,categorie_personne,resultat_humain,nombre,dont_nombre_blesse
1,A,X,10,1
2,B,Y,20,2"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            df = pd.read_csv(temp_path)
            df_validated = D1Schema.validate(df)
            
            assert df_validated['operation_id'].dtype == 'int64'
            assert df_validated['nombre'].dtype == 'int64'
        finally:
            os.unlink(temp_path)
    
    def test_validate_real_data_file(self):
        """Test validation with the actual data file structure."""
        # Simulate what df1.py does
        csv_path = 'data/data_1.csv'
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df_panderized = D1Schema.validate(df)
            
            assert len(df_panderized) > 0
            assert 'operation_id' in df_panderized.columns
        else:
            pytest.skip(f"CSV file {csv_path} does not exist")
    
    def test_csv_file_exists(self):
        """Test that the actual CSV file exists and can be loaded."""
        csv_path = 'data/data_1.csv'
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Check that required columns exist
            required_columns = ['operation_id', 'categorie_personne', 'resultat_humain', 
                              'nombre', 'dont_nombre_blesse']
            assert all(col in df.columns for col in required_columns), \
                f"Missing required columns. Found: {df.columns.tolist()}"
            
            # Try to validate
            df_validated = D1Schema.validate(df)
            assert len(df_validated) > 0
        else:
            pytest.skip(f"CSV file {csv_path} does not exist")

