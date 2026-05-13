import pandas as pd
import numpy as np
import datetime

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df,rupiah_exchange):
    df['Price'] = df['Price'].apply(lambda x: float(x))
    df['Price'] = (df['Price']*rupiah_exchange).astype(float)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df = df[df['Title'] != 'Unknown']
    # df['Timestamp'] = datetime.datetime.now()
    return df