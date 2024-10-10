import matplotlib.pyplot as plt

def run_eda(data):
    sales_trend = data.groupby('Date')['Total Sales'].sum()
    plt.figure(figsize=(12, 6))
    plt.plot(sales_trend.index, sales_trend.values, marker='o', linestyle='-', linewidth=1)
    plt.title('Sales Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.grid(True)
    plt.show()
