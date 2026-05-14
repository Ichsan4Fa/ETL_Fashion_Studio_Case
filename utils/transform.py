import pandas as pd
import numpy as np
import datetime

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df,rupiah_exchange):
    try:
        df['Price'] = df['Price'].str.replace(',', '').astype(float)
        df['Price'] = df['Price'].apply(lambda x: float(x))
        df['Price'] = (df['Price']*rupiah_exchange).astype(float)
        df['Rating'] = df['Rating'].apply(lambda x: float(x))
        df['Colors'] = df['Colors'].apply(lambda x: int(x))
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df = df[~df['Title'].str.contains('Unknown', case=False, na=False)]
        df['Timestamp'] = datetime.datetime.now()
    except Exception as e:
        print(f"Error occurs during transformation: {e}")
    return df