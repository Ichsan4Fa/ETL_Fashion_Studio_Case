import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import sys
import os

# Add utils to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.extract import fetch_data, extract_fashion_data, scrape_products


class TestFetchData:
    """Test cases for fetch_data function"""
    
    @patch('utils.extract.requests.Session')
    def test_fetch_data_success(self, mock_session):
        """Test successful data fetching"""
        mock_response = MagicMock()
        mock_response.text = "<html>Test HTML</html>"
        mock_response.raise_for_status = MagicMock()
        
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        result = fetch_data("http://example.com")
        
        assert result == "<html>Test HTML</html>"
        mock_session_instance.get.assert_called_once()
    
    @patch('utils.extract.requests.Session')
    def test_fetch_data_request_exception(self, mock_session):
        """Test fetch_data when request fails"""
        mock_session_instance = MagicMock()
        mock_session_instance.get.side_effect = Exception("Connection error")
        mock_session.return_value = mock_session_instance
        
        result = fetch_data("http://example.com")
        
        assert result is None


class TestExtractFashionData:
    """Test cases for extract_fashion_data function"""
    
    def test_extract_fashion_data_success(self):
        """Test successful extraction of fashion data"""
        html = """
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container">
                <span class="price">$100</span>
            </div>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Female</p>
        </div>
        """
        container = BeautifulSoup(html, "html.parser").find("div", class_="product-details")
        result = extract_fashion_data(container)
        
        assert result is not None
        assert result["Title"] == "Test Product"
        assert result["Price"] == "$100"
        assert result["Rating"] == "4.5"
        assert result["Colors"] == "3"
        assert result["Size"] == "M"
        assert result["Gender"] == "Female"
    
    def test_extract_fashion_data_missing_element(self):
        """Test extraction when required element is missing"""
        html = """
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
        </div>
        """
        container = BeautifulSoup(html, "html.parser").find("div", class_="product-details")
        result = extract_fashion_data(container)
        
        assert result is None


class TestScrapeProducts:
    """Test cases for scrape_products function"""
    
    @patch('utils.extract.fetch_data')
    @patch('utils.extract.time.sleep')
    def test_scrape_products_single_page(self, mock_sleep, mock_fetch):
        """Test scraping products from a single page"""
        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Product 1</h3>
                <div class="price-container">
                    <span class="price">$50</span>
                </div>
                <p>Rating: ⭐ 4 / 5</p>
                <p>2 Colors</p>
                <p>Size: S</p>
                <p>Gender: Male</p>
            </div>
        </div>
        """
        mock_fetch.return_value = html
        
        result = scrape_products("http://example.com", start_page=2, end_page=2)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert mock_fetch.called
    
    @patch('utils.extract.fetch_data')
    @patch('utils.extract.time.sleep')
    def test_scrape_products_empty_response(self, mock_sleep, mock_fetch):
        """Test scraping when API returns no data"""
        mock_fetch.return_value = None
        
        result = scrape_products("http://example.com", start_page=2, end_page=2)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    @patch('utils.extract.fetch_data')
    @patch('utils.extract.time.sleep')
    def test_scrape_products_with_custom_delay(self, mock_sleep, mock_fetch):
        """Test scraping with custom delay parameters"""
        html = "<div class='collection-card'></div>"
        mock_fetch.return_value = html
        
        result = scrape_products("http://example.com", start_page=2, end_page=2, min_delay=1, max_delay=2)
        
        assert mock_sleep.called
