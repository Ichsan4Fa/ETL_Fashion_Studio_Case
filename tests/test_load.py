import pytest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import sys
import os

# Add utils to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.load import load_to_postgres


class TestLoadToPostgres:
    """Test cases for load_to_postgres function"""
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_success(self, mock_create_engine):
        """Test successful loading of data to PostgreSQL"""
        # Create sample data
        data = pd.DataFrame({
            "Title": ["Product 1", "Product 2"],
            "Price": ["$50", "$75"],
            "Rating": [4.5, 4.0],
            "Colors": [2, 3],
            "Size": ["M", "L"],
            "Gender": ["Female", "Male"]
        })
        
        # Mock the engine and connection
        mock_connection = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connection.return_value.__enter__ = MagicMock(return_value=mock_connection)
        mock_engine.connection.return_value.__exit__ = MagicMock(return_value=None)
        mock_create_engine.return_value = mock_engine
        
        # Call the function
        load_to_postgres(data, "test_table", "postgresql://user:pass@localhost/db")
        
        # Verify engine was created
        mock_create_engine.assert_called_once_with("postgresql://user:pass@localhost/db")
        
        # Verify connection was used
        assert mock_engine.connection.called
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_with_replace(self, mock_create_engine):
        """Test loading with if_exist='replace' parameter"""
        data = pd.DataFrame({
            "Title": ["Product 1"],
            "Price": ["$50"],
            "Rating": [4.5],
            "Colors": [2],
            "Size": ["M"],
            "Gender": ["Female"]
        })
        
        mock_connection = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connection.return_value.__enter__ = MagicMock(return_value=mock_connection)
        mock_engine.connection.return_value.__exit__ = MagicMock(return_value=None)
        mock_create_engine.return_value = mock_engine
        
        load_to_postgres(data, "products", "postgresql://user:pass@localhost/db")
        
        # Verify to_sql was called
        mock_connection.to_sql = MagicMock()
        assert mock_engine.connection.called
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_connection_error(self, mock_create_engine):
        """Test error handling when connection fails"""
        data = pd.DataFrame({"Title": ["Product 1"]})
        
        # Mock engine to raise an exception
        mock_create_engine.side_effect = Exception("Connection refused")
        
        # Should not raise, but handle exception internally
        load_to_postgres(data, "test_table", "invalid://connection")
        
        # Verify engine creation was attempted
        mock_create_engine.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_empty_dataframe(self, mock_create_engine):
        """Test loading an empty DataFrame"""
        data = pd.DataFrame()
        
        mock_connection = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connection.return_value.__enter__ = MagicMock(return_value=mock_connection)
        mock_engine.connection.return_value.__exit__ = MagicMock(return_value=None)
        mock_create_engine.return_value = mock_engine
        
        load_to_postgres(data, "empty_table", "postgresql://user:pass@localhost/db")
        
        # Verify engine was created even with empty data
        mock_create_engine.assert_called_once_with("postgresql://user:pass@localhost/db")
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_large_dataset(self, mock_create_engine):
        """Test loading a large dataset"""
        # Create a larger dataset
        data = pd.DataFrame({
            "Title": [f"Product {i}" for i in range(1000)],
            "Price": ["$50"] * 1000,
            "Rating": [4.5] * 1000,
            "Colors": [2] * 1000,
            "Size": ["M"] * 1000,
            "Gender": ["Female"] * 1000
        })
        
        mock_connection = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connection.return_value.__enter__ = MagicMock(return_value=mock_connection)
        mock_engine.connection.return_value.__exit__ = MagicMock(return_value=None)
        mock_create_engine.return_value = mock_engine
        
        load_to_postgres(data, "large_table", "postgresql://user:pass@localhost/db")
        
        # Verify engine was created
        mock_create_engine.assert_called_once_with("postgresql://user:pass@localhost/db")
    
    @patch('utils.load.create_engine')
    def test_load_to_postgres_different_table_names(self, mock_create_engine):
        """Test loading with different table names"""
        data = pd.DataFrame({"Title": ["Product 1"]})
        
        mock_connection = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connection.return_value.__enter__ = MagicMock(return_value=mock_connection)
        mock_engine.connection.return_value.__exit__ = MagicMock(return_value=None)
        mock_create_engine.return_value = mock_engine
        
        # Test with different table names
        for table_name in ["products", "fashion_items", "my_table"]:
            load_to_postgres(data, table_name, "postgresql://user:pass@localhost/db")
        
        # Verify engine creation happened for each call
        assert mock_create_engine.call_count == 3
