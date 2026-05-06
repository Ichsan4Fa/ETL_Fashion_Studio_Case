import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add utils to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.transform import transform_to_dataframe, transform_data


class TestTransformToDataframe:
    """Test cases for transform_to_dataframe function"""
    
    def test_transform_to_dataframe_basic(self):
        """Test basic transformation of data to DataFrame"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Female"},
            {"Title": "Product 2", "Price": "$75", "Rating": "4.0", "Colors": "3", "Size": "L", "Gender": "Male"}
        ]
        
        df = transform_to_dataframe(data)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["Title", "Price", "Rating", "Colors", "Size", "Gender"]
    
    def test_transform_to_dataframe_empty_list(self):
        """Test transformation of empty list"""
        data = []
        
        df = transform_to_dataframe(data)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    def test_transform_to_dataframe_single_entry(self):
        """Test transformation of single entry"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Female"}
        ]
        
        df = transform_to_dataframe(data)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]["Title"] == "Product 1"


class TestTransformData:
    """Test cases for transform_data function"""
    
    def test_transform_data_type_conversion(self):
        """Test data type conversion"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Female"},
            {"Title": "Product 2", "Price": "$75", "Rating": "4.0", "Colors": "3", "Size": "L", "Gender": "Male"}
        ]
        df = transform_to_dataframe(data)
        
        transformed_df = transform_data(df, 16000)
        
        assert transformed_df["Rating"].dtype == float
        assert transformed_df["Colors"].dtype == int
        assert transformed_df["Size"].dtype == "string"
        assert transformed_df["Gender"].dtype == "string"
        assert transformed_df["Title"].dtype == "string"
    
    def test_transform_data_values_preserved(self):
        """Test that data values are preserved during transformation"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Female"}
        ]
        df = transform_to_dataframe(data)
        
        transformed_df = transform_data(df, 16000)
        
        assert transformed_df.iloc[0]["Title"] == "Product 1"
        assert transformed_df.iloc[0]["Price"] == "$50"
        assert transformed_df.iloc[0]["Rating"] == 4.5
        assert transformed_df.iloc[0]["Colors"] == 2
        assert transformed_df.iloc[0]["Size"] == "M"
        assert transformed_df.iloc[0]["Gender"] == "Female"
    
    def test_transform_data_with_different_exchange_rate(self):
        """Test transform_data with different exchange rates"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "4.5", "Colors": "2", "Size": "M", "Gender": "Female"}
        ]
        df = transform_to_dataframe(data)
        
        transformed_df = transform_data(df, 20000)  # Different exchange rate
        
        assert isinstance(transformed_df, pd.DataFrame)
        assert len(transformed_df) == 1
    
    def test_transform_data_numeric_strings_converted(self):
        """Test that numeric strings are properly converted"""
        data = [
            {"Title": "Product 1", "Price": "$50", "Rating": "3.2", "Colors": "5", "Size": "XL", "Gender": "Male"}
        ]
        df = transform_to_dataframe(data)
        
        transformed_df = transform_data(df, 16000)
        
        assert isinstance(transformed_df.iloc[0]["Rating"], float)
        assert isinstance(transformed_df.iloc[0]["Colors"], (int, np.integer))
