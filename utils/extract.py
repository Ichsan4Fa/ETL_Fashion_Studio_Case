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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"

    )
}

def fetch_data(url):
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504, 429],
        allowed_methods=["GET"]
    )
    session.mount("http://", HTTPAdapter(max_retries=retries))
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def extract_fashion_data(container):
    try:
        title = container.find("h3", class_="product-title").text
        price_span = container.find("div", class_="price-container")
        price = price_span.find("span", class_="price").text
        details = container.select("p")
        rating = details[0]
        color = details[1]
        size = details[2]
        gender = details[3]
        products = {
            "title": title,
            "price": price,
            "rating": rating,
            "color": color,
            "size": size,
            "gender": gender
        }
        return products
    except AttributeError as e:
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
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)  # Be polite and avoid overwhelming the server
    
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

def main():
    base_url = "https://fashion-studio.dicoding.dev"
    products = scrape_products(base_url)
    df = pd.DataFrame(products)
    if not df.empty:
        print(df.head())

if __name__ == "__main__":
    main()