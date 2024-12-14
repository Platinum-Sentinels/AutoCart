import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
import os
import re
import pandas as pd  # Import pandas for table formatting

# Load the environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_KEY')

# Positive and negative words list (extend this list as needed)
positive_words = ['good', 'great', 'excellent', 'amazing', 'best', 'fantastic', 'superb', 'outstanding', 'perfect', 'love']
negative_words = ['bad', 'poor', 'terrible', 'horrible', 'worst', 'disappointing', 'awful', 'mediocre', 'ugly', 'hate']

# Initialize WebDriver
def initialize_driver(chrome_driver_path, headless=False):
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
    
    return webdriver.Chrome(service=service, options=options)

# Function to optimize the search query using OpenAI GPT
def optimize_search_query(search_query):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Generate best search query to find the best most relevant products on an e-commerce website: {search_query}. Return only new search words. If any price ranges are mentioned, make sure to adjust the search to find products within that range.",
            max_tokens=50
        )
        optimized_query = response.choices[0].text.strip()
        print(f"Optimized Search Query: {optimized_query}")
        return optimized_query
    except Exception as e:
        print(f"Error optimizing query: {e}")
        return search_query  # Fallback to the original query if AI fails

# Custom sentiment analysis based on predefined words
def analyze_sentiment_using_keywords(page_text):
    sentiment_score = 0
    page_text = page_text.lower()
    
    for word in positive_words:
        sentiment_score += page_text.count(word)
    
    for word in negative_words:
        sentiment_score -= page_text.count(word)

    return sentiment_score

# Extract rating using regex pattern
def extract_rating_with_regex(page_text):
    matches = re.findall(r"(\d+\.\d+)\s+out of\s+5", page_text)
    if matches:
        return float(matches[0])
    return "No rating"

# Tag reference score calculation
def calculate_tag_reference_score(title, search_query):
    title = title.lower()
    search_query = search_query.lower().split()  # Split the search query into words

    tag_score = 0
    for word in search_query:
        if word in title:
            tag_score += 1  # Increase score for each word found in the title

    return tag_score

# Scrape Amazon
def scrape_amazon(search_query, chrome_driver_path, max_pages=3):
    driver = initialize_driver(chrome_driver_path)
    driver.get(f"https://www.amazon.com/s?k={search_query}")

    all_data = []
    for page in range(max_pages):
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-main-slot")]/div'))
            )
            product_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "s-main-slot")]/div')

            if not product_containers:
                print(f"No products found on page {page + 1}")
                break

            product_links = []
            for container in product_containers:
                try:
                    link = container.find_element(By.XPATH, './/a[@class="a-link-normal s-no-outline"]').get_attribute("href")
                    product_links.append(link)
                except Exception as e:
                    print(f"Skipping a container due to missing element: {e}")

            for link in product_links:
                driver.get(link)
                try:
                    name = driver.find_element(By.ID, 'productTitle').text
                    price = driver.find_element(By.XPATH, '//span[@class="a-price-whole"]').text if driver.find_elements(By.XPATH, '//span[@class="a-price-whole"]') else "Price not available"
                    
                    try:
                        rating_text = driver.find_element(By.XPATH, '//span[@class="a-icon-alt"]').text
                        rating = float(rating_text.split(' ')[0])
                    except Exception:
                        page_text = driver.page_source[:1000000]
                        rating = extract_rating_with_regex(page_text)

                    page_text = driver.page_source
                    sentiment_score = analyze_sentiment_using_keywords(page_text)
                    
                    # Calculate tag reference score based on product title and search query
                    tag_reference_score = calculate_tag_reference_score(name, search_query)

                    # New performance measure formula
                    performance_measure = (rating * 100 + sentiment_score * 100 + tag_reference_score * 100) / 300

                    all_data.append({
                        "Website": "Amazon", 
                        "Name": name, 
                        "Price": price, 
                        "Rating": rating, 
                        "Sentiment Score": sentiment_score, 
                        "Tag Reference Score": tag_reference_score,
                        "Performance Measure": performance_measure, 
                        "Link": link
                    })

                except Exception as e:
                    print(f"Error extracting product details: {e}")

            try:
                next_button = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]')
                next_button.click()
            except Exception:
                print("No more pages to scrape.")
                break

        except Exception as e:
            print(f"Error on page {page + 1}: {e}")
            break

    driver.quit()
    return all_data

# Scrape eBay
def scrape_ebay(search_query, max_pages=1):
    base_url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
    all_data = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}&_pgn={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.select(".s-item")

        if not items:
            print(f"No products found on eBay page {page}")
            break

        for item in items[:5]:
            try:
                name = item.select_one(".s-item__title").text
                price = item.select_one(".s-item__price").text
                link = item.select_one(".s-item__link")["href"]
                rating = item.select_one(".x-star-rating").text if item.select_one(".x-star-rating") else "No rating"

                review_text = item.select_one(".s-item__review").text if item.select_one(".s-item__review") else "No reviews"
                sentiment_score = analyze_sentiment_using_keywords(review_text)

                # Calculate tag reference score based on product title and search query
                tag_reference_score = calculate_tag_reference_score(name, search_query)

                # New performance measure formula
                performance_measure = (float(rating) * 100 + sentiment_score * 100 + tag_reference_score * 100) / 300 if rating != "No rating" else sentiment_score

                all_data.append({
                    "Website": "eBay", 
                    "Name": name, 
                    "Price": price, 
                    "Rating": rating, 
                    "Sentiment Score": sentiment_score, 
                    "Tag Reference Score": tag_reference_score,
                    "Performance Measure": performance_measure, 
                    "Link": link
                })

            except Exception as e:
                print(f"Error scraping eBay product: {e}")
                continue

    return all_data

# Search multiple websites and get results
def search_multiple_websites(search_query, chrome_driver_path, max_pages=1):
    optimized_query = optimize_search_query(search_query)  # Get optimized query from AI
    results_amazon = scrape_amazon(optimized_query, chrome_driver_path, max_pages)
    results_ebay = scrape_ebay(optimized_query, max_pages)

    return results_amazon + results_ebay

# Display results in table format and sort by performance measure
from tabulate import tabulate  # You can install this using: pip install tabulate

# Display results in a table format and sort by performance measure
def display_results(all_results):
    print("\nAggregated Results from All Websites (Sorted by Performance Measure):")
    if not all_results:
        print("No products found.")
        return

    # Convert to pandas DataFrame for better formatting
    df = pd.DataFrame(all_results)

    # Sort by performance measure (higher is better)
    df = df.sort_values(by="Performance Measure", ascending=False)

    # Use tabulate to display the results in a clearer table format
    table = tabulate(df, headers="keys", tablefmt="pretty", showindex=False)

    # Display the table
    print(table)
# Main Execution
if __name__ == "__main__":
    chrome_driver_path = "C:/Users/MUNIYA/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with your ChromeDriver path
    search_query = "msi katana gf66"  # Example search
    max_pages = 1

    results = search_multiple_websites(search_query, chrome_driver_path, max_pages)
    display_results(results)
