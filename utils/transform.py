import pandas as pd
import numpy as np
import timestamp

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df,rupiah_exchange):
    df['Price'] = (df['Price']*rupiah_exchange).astype(float)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df = df[df['Title'] != 'Unknown']
    df['Timestamp'] = timestamp.get_timestamp()
    return df