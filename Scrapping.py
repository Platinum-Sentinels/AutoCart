from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

# Initialize WebDriver
def initialize_driver(chrome_driver_path):
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=service, options=options)


# Scrape Amazon
def scrape_amazon(search_query, chrome_driver_path, max_pages=1):
    driver = initialize_driver(chrome_driver_path)
    base_url = f"https://www.amazon.com/s?k={search_query}"
    driver.get(base_url)
    all_data = []

    for page in range(max_pages):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-main-slot")]/div'))
            )
            product_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "s-main-slot")]/div')

            for container in product_containers[:5]:  # Limit to top 5 results per page
                try:
                    name = container.find_element(By.XPATH, './/h2/a/span').text
                    price = container.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
                    rating = container.find_element(By.XPATH, './/span[@class="a-icon-alt"]').text
                    link = container.find_element(By.XPATH, './/h2/a').get_attribute("href")
                    all_data.append({"Website": "Amazon", "Name": name, "Price": price, "Rating": rating, "Link": link})
                except Exception:
                    continue

            try:
                next_button = driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]')
                next_button.click()
                time.sleep(2)
            except Exception:
                break
        except Exception:
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

        for item in items[:5]:  # Limit to top 5 results per page
            try:
                name = item.select_one(".s-item__title").text
                price = item.select_one(".s-item__price").text
                link = item.select_one(".s-item__link")["href"]
                rating = item.select_one(".x-star-rating").text if item.select_one(".x-star-rating") else "No rating"
                all_data.append({"Website": "eBay", "Name": name, "Price": price, "Rating": rating, "Link": link})
            except Exception:
                continue

    return all_data


# Scrape Flipkart
def scrape_flipkart(search_query, chrome_driver_path, max_pages=1):
    driver = initialize_driver(chrome_driver_path)
    base_url = f"https://www.flipkart.com/search?q={search_query}"
    driver.get(base_url)
    all_data = []

    for page in range(max_pages):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "_1AtVbE")]'))
            )
            product_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "_1AtVbE")]')

            for container in product_containers[:5]:  # Limit to top 5 results per page
                try:
                    name = container.find_element(By.XPATH, './/div[contains(@class, "_4rR01T")]').text
                    price = container.find_element(By.XPATH, './/div[contains(@class, "_30jeq3")]').text
                    rating = container.find_element(By.XPATH, './/div[contains(@class, "_3LWZlK")]').text
                    link = container.find_element(By.XPATH, './/a').get_attribute("href")
                    all_data.append({"Website": "Flipkart", "Name": name, "Price": price, "Rating": rating, "Link": link})
                except Exception:
                    continue

            try:
                next_button = driver.find_element(By.XPATH, '//a[contains(@class, "_1LKTO3")]')
                next_button.click()
                time.sleep(2)
            except Exception:
                break
        except Exception:
            break

    driver.quit()
    return all_data


# Search multiple websites and get top results
def search_multiple_websites(search_query, chrome_driver_path, max_pages=1):
    results_amazon = scrape_amazon(search_query, chrome_driver_path, max_pages)
    results_ebay = scrape_ebay(search_query, max_pages)
    results_flipkart = scrape_flipkart(search_query, chrome_driver_path, max_pages)

    return results_amazon + results_ebay + results_flipkart


# Display results
def display_results(all_results):
    print("\nAggregated Results from All Websites:")
    for result in all_results:
        print(f"\nWebsite: {result['Website']}")
        print(f"Name: {result['Name']}")
        print(f"Price: {result['Price']}")
        print(f"Rating: {result['Rating']}")
        print(f"Link: {result['Link']}")

# Main Execution
if __name__ == "__main__":
    chrome_driver_path ="C:/Users/MUNIYA/Downloads/chromedriver-win64/chromedriver.exe" # Replace with your ChromeDriver path
    search_query = "laptop"  # Example search
    max_pages = 1

    results = search_multiple_websites(search_query, chrome_driver_path, max_pages)

    display_results(results)
