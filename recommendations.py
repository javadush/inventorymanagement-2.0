#recommendations.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import database_integration as dbi

def visualize_data(items, orders):
    quantities = [item[2] for item in items]
    prices = [item[3] for item in items]
    order_quantities = [order[2] for order in orders]

    plt.figure(figsize=(12, 6))

    # Scatter plot of quantities vs prices
    plt.subplot(1, 3, 1)
    plt.scatter(quantities, prices, color='blue')
    plt.xlabel('Quantity')
    plt.ylabel('Price')
    plt.title('Quantity vs Price')

    # Histogram of quantities
    plt.subplot(1, 3, 2)
    plt.hist(quantities, bins=20, color='green')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.title('Quantity Distribution')

    # Histogram of orders
    plt.subplot(1, 3, 3)
    plt.hist(order_quantities, bins=20, color='red')
    plt.xlabel('Order Quantity')
    plt.ylabel('Frequency')
    plt.title('Order Quantity Distribution')

    plt.tight_layout()
    plt.show()

def calculate_recommendations(items, orders):
    quantities = np.array([item[2] for item in items])
    prices = np.array([item[3] for item in items])
    order_quantities = np.array([order[2] for order in orders])

    # Example recommendation: correlation between quantity and price
    correlation, _ = pearsonr(quantities, prices)
    if correlation > 0.5:
        print("There is a positive correlation between quantity and price. Consider adjusting pricing strategies accordingly.")

    # Example recommendation: correlation between inventory and orders
    correlation_orders, _ = pearsonr(quantities, order_quantities)
    if correlation_orders > 0.5:
        print("There is a positive correlation between inventory levels and order quantities. Consider stocking up high-demand items.")

    # Example recommendation: stock level analysis
    mean_quantity = np.mean(quantities)
    std_quantity = np.std(quantities)

    if mean_quantity > 50 and std_quantity < 20:
        print("High average quantity and low variability suggest stable demand. Consider increasing stock levels to meet potential demand.")

    # Add more recommendations based on your specific analysis

def generate_recommendations():
    items = dbi.load_inventory_from_db()
    orders = dbi.load_orders_from_db()
    visualize_data(items, orders)
    calculate_recommendations(items, orders)

