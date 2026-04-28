import pandas as pd
import numpy as np

def transform_to_dataframe(data):
    df = pd.DataFrame(data)
    return df

def transform_data(df,rupiah_exchange):
    df['Rating'] = df['Rating'].str.replace('Rating: ⭐', '').astype(float)
    df['Colors'] = df['Colors'].str.replace(' Colors','').astype(int)
    df['Size'] = df['Size'].str.replace('Size: ','').astype('string')
    df['Gender'] = df['Gender'].str.replace('Gender: ','').astype('string')
    # df['Price_in_USD'] = df['Price'].apply(lambda x: float(x.replace("$", "")))
    # df['Price_in_IDR'] = (df['Price_in_USD']*rupiah_exchange).astype(float)
    
    df['Title'] = df['Title'].astype('string')
    # df['Price'] = df['Price'].astype(float)
    return df