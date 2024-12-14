import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
from dotenv import load_dotenv
import os
import re

# Load the environment variables
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_KEY')

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
            prompt=f"generate best search query to find the best most relevant products on an e-commerce website: {search_query} return only new search words only. If any price ranges are mentioned, make sure to adjust the search to find products within that range.",
            max_tokens=50
        )
        optimized_query = response.choices[0].text.strip()
        print(f"Optimized Search Query: {optimized_query}")
        return optimized_query
    except Exception as e:
        print(f"Error optimizing query: {e}")
        return search_query  # Fallback to the original query if AI fails

# Scrape Amazon
def extract_rating_with_regex(page_text):
    # Search for "X.X out of 5" pattern in the text
    matches = re.findall(r"(\d+\.\d+)\s+out of\s+5", page_text)
    if matches:
        return float(matches[0])  # Return the first valid match
    return "No rating"  # Default if no matches found

def scrape_amazon(search_query, chrome_driver_path, max_pages=3):
    driver = initialize_driver(chrome_driver_path)
    driver.get(f"https://www.amazon.com/s?k={search_query}")

    all_data = []
    for page in range(max_pages):
        try:
            # Wait until the product containers are loaded on the page
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

            # Extract details from each product link
            for link in product_links:
                driver.get(link)
                try:
                    # Extract product name
                    name = driver.find_element(By.ID, 'productTitle').text

                    # Extract product price
                    try:
                        price = driver.find_element(By.XPATH, '//span[@class="a-price-whole"]').text
                    except Exception:
                        price = "Price not available"

                    # Extract product rating using direct method
                    try:
                        rating_text = driver.find_element(By.XPATH, '//span[@class="a-icon-alt"]').text
                        rating = float(rating_text.split(' ')[0])  # Extract numerical rating
                    except Exception:
                        # Fallback: Extract all page text and use regex-based rating extraction
                        page_text = driver.page_source[:1000000]  # Limit text to 1MB for processing
                        rating = extract_rating_with_regex(page_text)

                    all_data.append({"Website": "Amazon", "Name": name, "Price": price, "Rating": rating, "Link": link})
                except Exception as e:
                    print(f"Error extracting product details: {e}")

            # Navigate to the next page
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
                all_data.append({"Website": "eBay", "Name": name, "Price": price, "Rating": rating, "Link": link})
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

# Display results
def display_results(all_results):
    print("\nAggregated Results from All Websites:")
    if not all_results:
        print("No products found.")
        return

    for result in all_results:
        website = result.get('Website', 'N/A')
        name = result.get('Name', 'N/A')
        price = result.get('Price', 'N/A')
        rating = result.get('Rating', 'N/A')
        link = result.get('Link', 'N/A')

        print(f"\nWebsite: {website}")
        print(f"Name: {name}")
        print(f"Price: {price}")
        print(f"Rating: {rating}")
        print(f"Link: {link}")

# Main Execution
if __name__ == "__main__":
    chrome_driver_path = "C:/Users/MUNIYA/Downloads/chromedriver-win64/chromedriver.exe"  # Replace with your ChromeDriver path
    search_query = "msi katana gf66"  # Example search
    max_pages = 1

    # Set headless to False for visual inspection in Chrome
    results = search_multiple_websites(search_query, chrome_driver_path, max_pages)

    display_results(results)
