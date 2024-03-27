import time
import mysql.connector
from mysql.connector import Error
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

# Accept cookies if the button exists
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

# Connect to MySQL database
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='dealabs',
        user='root',
        password=''
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS offers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            price VARCHAR(50),
            company_name VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)

        # Loop through each offer element
        for offer_element in offer_elements:
            try:
                # Extract information
                title = offer_element.find_element("xpath", ".//strong[contains(@class, 'thread-title')]/a").get_attribute('title')
                price = offer_element.find_element("xpath", ".//span[contains(@class, 'threadItemCard-price')]").text
                company_name = offer_element.find_element("xpath", ".//button[@data-t='merchantLink']").text.strip()

                # Insert data into MySQL table
                insert_query = "INSERT INTO offers (title, price, company_name) VALUES (%s, %s, %s)"
                data = (title, price, company_name)
                cursor.execute(insert_query, data)
                connection.commit()

            except Exception as e:
                pass

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close all connections
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

# Quit the driver
driver.quit()
