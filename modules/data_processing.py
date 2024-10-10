import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

def clean_data(data):
    data = data.drop_duplicates()
    data = data.fillna(method='ffill')
    return data

def feature_engineering(data):
    data['Month'] = data['Date'].dt.to_period('M')
    data['Quarter'] = data['Date'].dt.to_period('Q')
    return data
