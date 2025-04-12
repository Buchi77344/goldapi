import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run headlessly (no UI)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Automatically download the correct version of ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# List of gold jewelry companies to scrape
companies_to_scrape = [
    "https://www.inven.ai/company-lists/top-26-gold-jewelry-companies",
    "https://www.grandviewresearch.com/industry-analysis/gold-jewelry-market"
    # Add more URLs here...
]

company_data = []

for url in companies_to_scrape:
    driver.get(url)
    time.sleep(3)
    
    # Wait for the page to fully load
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        print(f"Successfully loaded page {url}")
    except Exception as e:
        print(f"Timeout while waiting for page {url} to load:", e)
        continue
    
    # Extract company name, email, domain, address, country (example)
    try:
        company_name = driver.find_element(By.CSS_SELECTOR, "h1").text
        business_address = "Address not found"
        country = "Country not found"
        
        # Look for email
        body_text = driver.page_source
        email_matches = re.findall(r'[\w\.-]+@[\w\.-]+', body_text)
        email = email_matches[0] if email_matches else "Email not found"
        
        # Extract company domain (if possible)
        domain = "Domain not found"
        if "http" in body_text:
            url_matches = re.findall(r'https?://([A-Za-z_0-9.-]+).*', body_text)
            if url_matches:
                domain = url_matches[0]
        
        company_data.append([company_name, email, domain, business_address, country])
    
    except Exception as e:
        print(f"Error scraping data from {url}: {e}")
        continue

# Save data to CSV
csv_file = 'company_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name', 'Email', 'Domain', 'Business Address', 'Country'])
    writer.writerows(company_data)

# Clean up
driver.quit()

csv_file
