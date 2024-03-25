import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.lemonde.fr/actualite-en-continu/"

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all articles
articles = soup.find_all('h3', class_='teaser__title')

# Iterate through each article and extract its title and description
for article in articles:
    # Extract the title
    title = article.text.strip()
    
    # Extract the description
    description = article.find_next('p', class_='teaser__desc').text.strip()
    
    # Print the title and description
    print("Title:", title)
    print("Description:", description)
    print()
