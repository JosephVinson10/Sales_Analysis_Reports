import os
from modules.data_processing import load_data, clean_data, feature_engineering
from modules.eda import run_eda
from modules.forecasting import build_forecasting_model

def main():
    print("Loading data...")
    file_path = 'data/synthetic_sales_data.csv'
    data = load_data(file_path)
    print("Data loaded successfully.")

    print("Cleaning data...")
    cleaned_data = clean_data(data)
    print("Data cleaned successfully.")

    print("Enhancing data with feature engineering...")
    enhanced_data = feature_engineering(cleaned_data)
    print("Feature engineering completed.")

    print("Running Exploratory Data Analysis (EDA)...")
    run_eda(enhanced_data)
    print("EDA completed successfully.")

    print("Building forecasting model...")
    build_forecasting_model(enhanced_data)
    print("Forecasting model built successfully.")

    print("Launching Streamlit Dashboard...")
    os.system("streamlit run modules/dashboard.py")

if __name__ == '__main__':
    main()
