import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'welcome_jungle'
}

# Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")

# Use ChromeDriverManager to automatically download and manage chromedriver
driver_path = ChromeDriverManager().install()
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.welcometothejungle.com/fr/jobs?page=1&refinementList%5Bprofession_name.fr.Tech%5D%5B%5D=Data%20Analysis&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI')
time.sleep(5)

# Extract job information
job_elements = driver.find_elements(By.XPATH, "//li[@data-testid='search-results-list-item-wrapper']")
for job_element in job_elements:
    job_title = job_element.find_element(By.XPATH, ".//h4").text
    company_name = job_element.find_element(By.XPATH, ".//span[@class='sc-ERObt ldmfCZ sc-6i2fyx-3 eijbZE wui-text']").text
    location = job_element.find_element(By.XPATH, ".//span[@class='sc-68sumg-0 gvkFZv']").text
    
    # Insert job information into the database
    insert_query = "INSERT INTO jobs (job_title, company_name, location) VALUES (%s, %s, %s)"
    insert_values = (job_title, company_name, location)
    cursor.execute(insert_query, insert_values)
    conn.commit()

    print(f"Job Title: {job_title}\nCompany Name: {company_name}\nLocation: {location}\n")

# Close database connection
cursor.close()
conn.close()

driver.quit()
