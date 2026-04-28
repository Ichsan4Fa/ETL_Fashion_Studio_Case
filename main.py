import pandas as pd

from utils.extract import fetch_data, scrape_products, extract_fashion_data
from utils.transform import transform_to_dataframe, transform_data

def main():
    base_url = "https://fashion-studio.dicoding.dev"
    products = scrape_products(base_url)
    if products:
        df = transform_to_dataframe(products)
        print(f"Scraped data:")
        print(df.head())
        transform_df = transform_data(df, rupiah_exchange = 17500)
        print(f"Transformed data: ")
        print(transform_df.head())
    
if __name__ == "__main__":
    main()