from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Configure FireFox Webdriver
driver_path = "/home/aki/webscraping/geckodriver-v0.35.0-linux64/geckodriver"
service = Service(driver_path)
firefox_options = webdriver.FirefoxOptions()

# Initialize the main driver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Get the main page with all product links
driver.get("https://www.ultrapc.ma/150-pc-portables-gamer")
time.sleep(3)  # Allow time for the page to load

csv_file = "ultrapc_laptops.csv"

try:
    # Collect all product links
    anchor_divs = driver.find_elements(By.XPATH, '//h3[@class="product-title"]/a')
    all_h_links = [anchor_div.get_attribute('href') for anchor_div in anchor_divs]
finally:
    driver.quit()

# Function to extract data from a product page
def extract_data(driver_object):
    """Extracts product information."""
    data = {}

    try:
        # Wait for the product title
        data['Description'] = WebDriverWait(driver_object, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@class="product-title"]'))
        ).text

        # Extract additional product details
        try:
            data['Status'] = driver_object.find_element(
                By.XPATH, '//div[@class="control-item py-1 float-right font-weight-bold"]').text
        except:
            data['Status'] = "N/A"

        try:
            data['Price'] = driver_object.find_element(By.XPATH, '//span[@class="price"]').text
        except:
            data['Price'] = "N/A"

        try:
            data['Reference'] = driver_object.find_element(By.XPATH, '//span[@class="font-weight-bold"]').text
        except:
            data['Reference'] = "N/A"

        try:
            data['Availability'] = driver_object.find_element(By.XPATH, '//span[contains(@class, "product-available")]').text
        except:
            data['Availability'] = "N/A"

        # Extract product specifications
        specs_name = driver_object.find_elements(By.XPATH, '//dt[@class="name mb-1 p-2"]')
        specs_value = driver_object.find_elements(By.XPATH, '//dd[@class="value mb-1 p-2"]')
        for name, value in zip(specs_name, specs_value):
            data[name.text] = value.text

    except Exception as e:
        print(f"Error extracting data: {e}")

    return data


# Process each product link and extract data
laptops_info = []

with webdriver.Firefox(service=service, options=firefox_options) as driver2:
    for hlink in all_h_links:
        try:
            driver2.get(hlink)
            product_info = extract_data(driver2)
            laptops_info.append(product_info)
        except Exception as e:
            print(f"Error processing link {hlink}: {e}")

# Generate dynamic headers
headers = set()
for laptop in laptops_info:
    headers.update(laptop.keys())

headers = list(headers)

# Write data to a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(laptops_info)
