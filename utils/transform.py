import pandas as pd
import numpy as np
import datetime

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df,rupiah_exchange):
    try:
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df = df[~df['Title'].str.contains('Unknown', case=False, na=False)]
        df.loc[:, 'Price'] = df['Price'].str.replace('$', '', regex=False)
        df.loc[:, 'Price'] = df['Price'].astype(float)
        df.loc[:, 'Price'] = (df['Price']*rupiah_exchange).astype(float)
        df.loc[:, 'Rating'] = df['Rating'].apply(lambda x: float(x))
        df.loc[:, 'Colors'] = df['Colors'].apply(lambda x: int(x))
        df.loc[:, 'Title'] = df['Title'].astype('string')
        df.loc[:, 'Size'] = df['Size'].astype('string')
        df.loc[:, 'Gender'] = df['Gender'].astype('string')
        df['Timestamp'] = pd.Timestamp.now()
        # Ensure proper dtypes after operations
        df = df.astype({'Rating': float, 'Colors': int, 'Title': 'string', 'Size': 'string', 'Gender': 'string'})
    except Exception as e:
        print(f"Error occurs during transformation: {e}")
    return df