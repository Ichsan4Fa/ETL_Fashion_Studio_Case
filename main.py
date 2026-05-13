import pandas as pd

from utils.extract import fetch_data, scrape_products, extract_fashion_data
from utils.transform import transform_to_dataframe, transform_data
from utils.load import load_to_postgres

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
        print("Data transformation successful.")
    # try:
    #     load_to_csv(transform_df, "transformed_data.csv")
    #     print("Data loaded to CSV successfully.")
    #     load_to_database(transform_df, "fashion_data.db", "postgresql://username:password@localhost:5432/mydatabase")
    # except Exception as e:
    #     print(f"Error occurred while loading data: {e}")

if __name__ == "__main__":
    main()