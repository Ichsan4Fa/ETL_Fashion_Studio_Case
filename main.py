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
            print(df.shape)
            transform_df = transform_data(df, rupiah_exchange = 16000)
            print(f"Transformed data: ")
            print(transform_df.head())
            print(transform_df.shape)
        except Exception as e:
            print(f"Error occurred while transforming data: {e}")
    else:
        print("No data to transform.")
    
    try:
        load_to_csv(transform_df, "products.csv")
        print("Data loaded to CSV successfully.")
        load_to_postgres(transform_df, "products", "postgresql://[username]:[password]@localhost:[port]/[dbname]")
        load_to_google_sheets(transform_df, "[spreadsheets_id]", "Sheet1", "google-sheets-api.json")
    except Exception as e:
        print(f"Error occurred while loading data: {e}")

if __name__ == "__main__":
    main()
