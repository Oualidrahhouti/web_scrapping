import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Showing some data requires dealing with cookies, so the code below refuse cookies to hide that div
try:
    cookie_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@data-t='continueWithoutAcceptingBtn']")))
    cookie_button.click()
except:
    pass

# Wait for the offers to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, "//article[contains(@class, 'thread')]")))

# Find all offer elements
offer_elements = driver.find_elements("xpath", "//article[contains(@class, 'thread')]")

# Loop through each offer element
for offer_element in offer_elements:
    try:
        # Extract information
        title = offer_element.find_element("xpath", ".//strong[contains(@class, 'thread-title')]/a").get_attribute('title')
        price = offer_element.find_element("xpath", ".//span[contains(@class, 'threadItemCard-price')]").text
        company_name = offer_element.find_element("xpath", ".//button[@data-t='merchantLink']").text.strip()

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
