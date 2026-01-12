import pytest
import pandas as pd
import pandera.errors
from df1_pandera_schema import D1Schema


class TestD1Schema:
    """Test cases for D1Schema validation."""
    
    def test_schema_validation_success(self):
        """Test that valid data passes schema validation."""
        valid_data = pd.DataFrame({
            'operation_id': [1, 2, 3],
            'categorie_personne': ['A', 'B', 'C'],
            'resultat_humain': ['X', 'Y', 'Z'],
            'nombre': [10, 20, 30],
            'dont_nombre_blesse': [1, 2, 3]
        })
        
        validated_df = D1Schema.validate(valid_data)
        
        assert len(validated_df) == 3
        assert list(validated_df.columns) == ['operation_id', 'categorie_personne', 
                                             'resultat_humain', 'nombre', 'dont_nombre_blesse']
        assert validated_df['operation_id'].dtype == 'int64'
        assert validated_df['categorie_personne'].dtype == 'object'
        assert validated_df['nombre'].dtype == 'int64'
    
    def test_schema_validation_with_coercion(self):
        """Test that schema coerces types correctly."""
        data_with_string_numbers = pd.DataFrame({
            'operation_id': ['1', '2', '3'],
            'categorie_personne': ['A', 'B', 'C'],
            'resultat_humain': ['X', 'Y', 'Z'],
            'nombre': ['10', '20', '30'],
            'dont_nombre_blesse': ['1', '2', '3']
        })
        
        validated_df = D1Schema.validate(data_with_string_numbers)
        
        assert validated_df['operation_id'].dtype == 'int64'
        assert validated_df['nombre'].dtype == 'int64'
        assert validated_df['dont_nombre_blesse'].dtype == 'int64'
    
    def test_schema_validation_missing_column(self):
        """Test that missing columns raise validation error."""
        invalid_data = pd.DataFrame({
            'operation_id': [1, 2, 3],
            'categorie_personne': ['A', 'B', 'C'],
            'resultat_humain': ['X', 'Y', 'Z'],
            'nombre': [10, 20, 30]
            # Missing 'dont_nombre_blesse'
        })
        
        with pytest.raises(pandera.errors.SchemaError):
            D1Schema.validate(invalid_data)
    
    def test_schema_validation_wrong_type(self):
        """Test that wrong types raise validation error."""
        invalid_data = pd.DataFrame({
            'operation_id': ['not_a_number', '2', '3'],
            'categorie_personne': ['A', 'B', 'C'],
            'resultat_humain': ['X', 'Y', 'Z'],
            'nombre': [10, 20, 30],
            'dont_nombre_blesse': [1, 2, 3]
        })
        
        with pytest.raises(pandera.errors.SchemaError):
            D1Schema.validate(invalid_data)
    
    def test_schema_validation_empty_dataframe(self):
        """Test that empty dataframe passes validation."""
        empty_data = pd.DataFrame({
            'operation_id': [],
            'categorie_personne': [],
            'resultat_humain': [],
            'nombre': [],
            'dont_nombre_blesse': []
        })
        
        validated_df = D1Schema.validate(empty_data)
        
        assert len(validated_df) == 0
        assert list(validated_df.columns) == ['operation_id', 'categorie_personne', 
                                             'resultat_humain', 'nombre', 'dont_nombre_blesse']

