import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

def run_dashboard(data):
    st.title('Sales Data Analysis Dashboard with Overall Sales Forecasting')

    st.header('Sales Data Overview')

    # Interactive filters for date range and region
    st.sidebar.header('Filter Options')
    date_range = st.sidebar.date_input('Select Date Range', 
                                       [data['Date'].min(), data['Date'].max()])
    selected_region = st.sidebar.multiselect('Select Region', 
                                             options=data['Region'].unique(), 
                                             default=data['Region'].unique())

    # Apply filters to the data
    filtered_data = data[(data['Date'] >= pd.to_datetime(date_range[0])) & 
                         (data['Date'] <= pd.to_datetime(date_range[1]))]
    filtered_data = filtered_data[filtered_data['Region'].isin(selected_region)]

    st.write('Here is a preview of the filtered sales data:')
    st.dataframe(filtered_data.head())

    # Sales Trend Over Time with 30-Day Forecast (Overall)
    st.header('Overall Sales Trend with 30-Day Forecast')
    sales_trend = filtered_data.groupby('Date')['Total Sales'].sum().reset_index()
    sales_trend['Days'] = (sales_trend['Date'] - sales_trend['Date'].min()).dt.days
    X = sales_trend['Days'].values.reshape(-1, 1)
    y = sales_trend['Total Sales'].values

    # Train the Linear Regression model for overall sales forecast
    model = LinearRegression()
    model.fit(X, y)

    # Forecast overall sales for the next 30 days
    future_days = np.arange(X[-1][0] + 1, X[-1][0] + 31).reshape(-1, 1)
    future_sales = model.predict(future_days)
    future_dates = pd.date_range(sales_trend['Date'].iloc[-1] + pd.Timedelta(days=1), periods=30)

    # Plot historical sales and forecasted sales (Overall)
    forecast_df = pd.DataFrame({'Date': future_dates, 'Total Sales': future_sales})
    fig_forecast = px.line(sales_trend, x='Date', y='Total Sales', title='Overall Sales Trend with 30-Day Forecast')
    fig_forecast.add_scatter(x=forecast_df['Date'], y=forecast_df['Total Sales'], mode='lines', name='Forecast')

    # Update layout for better visualization
    fig_forecast.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Sales ($)',
        legend_title='Legend',
        template='plotly_white',
        hovermode='x unified'
    )

    st.plotly_chart(fig_forecast)

    # Total Sales by Region
    st.header('Total Sales by Region')
    region_sales = filtered_data.groupby('Region')['Total Sales'].sum().reset_index()
    fig_region_sales = px.bar(region_sales, x='Region', y='Total Sales', title='Total Sales by Region')
    st.plotly_chart(fig_region_sales)

    # Top 10 Products by Sales
    st.header('Top 10 Products by Total Sales')
    product_sales = filtered_data.groupby('Product Name')['Total Sales'].sum().sort_values(ascending=False).reset_index()
    fig_top_products = px.bar(product_sales.head(10), x='Product Name', y='Total Sales', title='Top 10 Products by Total Sales')
    st.plotly_chart(fig_top_products)

    # Impact of Discounts on Sales
    st.header('Impact of Discounts on Average Sales')
    discount_sales = filtered_data.groupby('Discount Percentage')['Total Sales'].mean().reset_index()
    fig_discount_impact = px.line(discount_sales, x='Discount Percentage', y='Total Sales', title='Impact of Discounts on Average Sales')
    st.plotly_chart(fig_discount_impact)

# Load the sales data
data = pd.read_csv('data/synthetic_sales_data.csv')
data['Date'] = pd.to_datetime(data['Date'])  # Convert the Date column to datetime format
run_dashboard(data)
