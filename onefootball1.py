from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

# Configure FireFox Webdriver
driver_path = "/home/aki/webscraping/geckodriver-v0.35.0-linux64/geckodriver"
service = Service(driver_path)
firefox_options = webdriver.FirefoxOptions()

# Initialize the main driver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Get the main page with all match links
driver.get("https://www.footmercato.net/live/europe/2025-01-21")
time.sleep(3)  # Allow time for the page to load

csv_file = "data.csv"


try:
    # Collect all match links
    anchor_divs = driver.find_elements(By.XPATH, "//div[@class='matchFull']/a")
    all_h_links = [anchor_div.get_attribute('href') for anchor_div in anchor_divs]
finally:
    driver.quit()

# Function to scroll the page for animation (optional)
def animate_scroll(driver_object):
    """Scrolls the web page down for a smooth animation."""
    for _ in range(3):  # Repeat the scroll three times
        time.sleep(1)
        driver_object.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

# Function to extract data from a match page
def extract_data(driver_object):
    """Extracts general information about the match."""
    try:
        # Wait for the match info to load
        match_kind = WebDriverWait(driver_object, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='matchTopBar__competitionName']"))
        ).text

        teams = driver_object.find_elements(By.XPATH, '//span[@class="scoreboard__teamName"]')
        team1 = teams[0].text if len(teams) > 0 else "N/A"
        team2 = teams[1].text if len(teams) > 1 else "N/A"

        score = driver_object.find_element(By.XPATH, '//div[@class="scoreboard__score scoreboard__score--played"]').text

        print(f"{match_kind}: {team1} vs {team2} - {score}")
        return [match_kind, team1, team2, score]

    except Exception as e:
        print(f"Error extracting match data: {e}")
        return ["N/A", "N/A", "N/A", "N/A"]

# Process each match link and extract data
all_matches_general_info = []

for hlink in all_h_links:
    driver2 = webdriver.Firefox(service=service, options=firefox_options)
    try:
        driver2.get(hlink)
        general_info = extract_data(driver2)
        all_matches_general_info.append(general_info)
        animate_scroll(driver2)
    except Exception as e:
        print(f"Error processing link {hlink}: {e}")
    finally:
        driver2.quit()

# Output the results

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['League', 'Team1', 'Team2', 'Score'])
        writer.writerows(all_matches_general_info)


