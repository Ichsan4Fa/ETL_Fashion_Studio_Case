import pandas as pd

from utils.extract import fetch_data, scrape_products, extract_fashion_data
from utils.transform import transform_to_dataframe, transform_data
from utils.load import load_to_postgres, load_to_csv, load_to_google_sheets

def main():
    try:
        base_url = "https://fashion-studio.dicoding.dev"
        products = scrape_products(base_url)
    except Exception as e:
        print(f"Error occurred while scraping products: {e}")

    if products:
        try:
            df = transform_to_dataframe(products)
            print(f"Scraped data:")
            print(df.head())
            transform_df = transform_data(df, rupiah_exchange = 16000)
            print(f"Transformed data: ")
            print(transform_df.head())
        except Exception as e:
            print(f"Error occurred while transforming data: {e}")
    else:
        print("No data to transform.")
    
    try:
        load_to_csv(transform_df, "transformed_data.csv")
        print("Data loaded to CSV successfully.")
        load_to_postgres(transform_df, "postgresql://developer:supersecretpassword@localhost:5432/productdb")
        load_to_google_sheets(transform_df, "1a2b3c4d5e6f7g8h9i0j", "Sheet1", "credentials.json")
    except Exception as e:
        print(f"Error occurred while loading data: {e}")

if __name__ == "__main__":
    main()