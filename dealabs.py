import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")

# Use ChromeDriverManager to automatically download and manage chromedriver
driver_path = ChromeDriverManager().install()
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# URL of the webpage containing the offer details
url = 'https://www.dealabs.com/'

# Open the webpage
driver.get(url)
time.sleep(20)  # Add a delay to ensure the page is fully loaded

# Find all offer elements
offer_elements = driver.find_elements("xpath", "//article[contains(@class, 'thread')]")

# Loop through each offer element
for offer_element in offer_elements:
    try:
        # Extract information
        title = offer_element.find_element("xpath", ".//strong[contains(@class, 'thread-title')]/a").get_attribute('title')
        price_element = offer_element.find_element("xpath", ".//span[contains(@class, 'threadItemCard-price')]")
        price = price_element.text if price_element.text else "Price not available"
        company_name_element = offer_element.find_element("xpath", ".//button[@data-t='merchantLink']")
        company_name = company_name_element.text.strip() if company_name_element.text else "Company name not available"

        # Print extracted information
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Company Name: {company_name}")
        print("")

    except Exception as e:
        print("Error occurred while scraping an offer:")
        print(e)
        print("")

# Quit the driver
driver.quit()
