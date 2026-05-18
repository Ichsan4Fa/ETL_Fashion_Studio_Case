import time
import pandas as pd
import requests
import random

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

HEADERS ={
    "User-Agent" : 
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}

def fetch_data(url, max_retries=7):
    session = requests.Session()
    retries = Retry(
        total=max_retries,
        backoff_factor=2,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    for attempt in range(3):
        try:
            response = session.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.ConnectionError as e:
            if attempt < 2:
                wait_time = random.uniform(5, 10)
                print(f"Connection error (attempt {attempt+1}/3), retrying in {wait_time:.1f}s: {e}")
                time.sleep(wait_time)
            else:
                print(f"Error fetching data from {url} after 3 attempts: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            return None
    return None

def extract_fashion_data(container):
    try:
        if not container:
            return None
        
        title_elem = container.find("h3", class_="product-title")
        if not title_elem:
            return None
        title = title_elem.text
        
        price_span = container.find("div", class_="price-container")
        if price_span:
            price_elem = price_span.find("span", class_="price")
            price = price_elem.text if price_elem else None
        else:
            price = None
        
        details = container.select("p")
        if len(details) < 4:
            return None
        
        rating = details[0].text.replace('Rating: ⭐ ', '').replace(' / 5','').strip() or None
        color = details[1].text.replace(' Colors','').strip() or None
        size = details[2].text.replace('Size: ','').strip() or None
        gender = details[3].text.replace('Gender: ','').strip() or None
        products = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": color,
            "Size": size,
            "Gender": gender
        }
        return products
    except (AttributeError, IndexError) as e:
        print(f"Error extracting data: {e}")
        return None
    
def scrape_products(base_url, start_page=2, end_page=50, min_delay=3, max_delay=5):
    all_products = []

    # Extract the first page
    html_content = fetch_data(base_url)
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        collection_cards = soup.find_all("div", class_="collection-card")
        for card in collection_cards:
            product_containers = card.find_all("div", class_="product-details")
            for container in product_containers:
                product_data = extract_fashion_data(container)
                if product_data:
                    all_products.append(product_data)
    
    # Extract subsequent pages
    for page in range(start_page, end_page + 1):
        url = f"{base_url}/page{page}"
        html_content = fetch_data(url)
        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            collection_cards = soup.find_all("div", class_="collection-card")
            for card in collection_cards:
                product_containers = card.find_all("div", class_="product-details")
                for container in product_containers:
                    product_data = extract_fashion_data(container)
                    if product_data:
                        all_products.append(product_data)
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)  # Be polite and avoid overwhelming the server        
    return all_products