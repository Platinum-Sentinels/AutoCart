import pandas as pd
import re
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from Scrapping import search_multiple_websites

# PerformanceAgent class for scoring
class PerformanceAgent:
    def __init__(self):
        # Initialize a simple model with mock training data
        self.model = RandomForestRegressor()
        self._train_mock_model()

    def _train_mock_model(self):
        # Mock training data for demonstration
        X_train = pd.DataFrame({
            "Rating": [4.5, 3.8, 5.0, 0.0],
            "Price": [75.0, 20.0, 120.0, 50.0],
            "Tag_Relevance": [0.9, 0.6, 0.95, 0.4]
        })
        y_train = [0.85, 0.7, 0.95, 0.5]  # Corresponding performance scores
        self.model.fit(X_train, y_train)

    def measure_performance(self, product_data):
        # Preprocess the product data
        product_data = preprocess_product_data(product_data)

        # Ensure required columns
        required_columns = ["Rating", "Price", "Tag_Relevance"]
        for col in required_columns:
            if col not in product_data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Predict performance scores
        predictions = self.model.predict(product_data[required_columns])

        # Attach predictions to the DataFrame
        product_data["Performance_Score"] = predictions
        return product_data


# Preprocessing function to clean and prepare the data
def preprocess_product_data(product_data):
    """
    Preprocess the product data to include tags, numeric columns, and other relevant data.
    """
    # Clean Rating
    product_data["Rating"] = product_data["Rating"].apply(
        lambda x: float(x) if isinstance(x, (int, float)) else 0.0
    )

    # Parse Price
    product_data["Price"] = product_data["Price"].apply(parse_price)

    # Create Tag Relevance (mock logic: relevance of "Laptop Charger" or similar keywords)
    product_data["Tag_Relevance"] = product_data["Name"].apply(
        lambda name: compute_tag_relevance(name, ["Laptop Charger", "MSI", "Katana"])
    )

    return product_data


# Function to parse price
def parse_price(price):
    if isinstance(price, str):
        price = re.sub(r"[^\d.]", "", price)  # Remove non-numeric characters
        return float(price) if price else 0.0
    return float(price) if isinstance(price, (int, float)) else 0.0


# Function to compute tag relevance
def compute_tag_relevance(name, tags):
    if not isinstance(name, str):
        return 0.0
    relevance = sum([1 for tag in tags if tag.lower() in name.lower()]) / len(tags)
    return round(relevance, 2)


# Example search results
# search_results = [
#     {"Website": "Amazon", "Name": "KFD 240W 20V 12A Laptop Charger for MSI GF66 GF76 GL66 GL76 GS66 MSI Katana", "Price": "75.0", "Rating": 4.5, "Link": "https://amazon.com/product1"},
#     {"Website": "eBay", "Name": "Shop on eBay", "Price": "20.0", "Rating": 0.0, "Link": "https://ebay.com/product2"}
# ]


# Main execution
if __name__ == "__main__":
    chrome_driver_path = "C:/Users/MUNIYA/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with your ChromeDriver path
    # Convert search results to a DataFrame
    search_query = "msi katana gf66"  # Example search
    max_pages = 1

    # Set headless to False for visual inspection in Chrome
    results = search_multiple_websites(search_query, chrome_driver_path, max_pages)
    product_data = pd.DataFrame(results)

    # Initialize PerformanceAgent
    agent = PerformanceAgent()

    # Score the products
    scored_products = agent.measure_performance(product_data)

    # Display results
    print("\nScored Product Results:")
    print(scored_products)
