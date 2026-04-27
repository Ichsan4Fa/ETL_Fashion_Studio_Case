import pandas as pd
import numpy as np


def transform_cols(df):
    df['Rating'] = df['Rating'].str.replace(' out of 5 stars', '').astype(float)
    df['Price_in_IDR'] = df['Price'].str.replace('Rp', '').str.replace('.', '').astype(float)*17000
    return df