import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.kebab-frites.com/meilleur-kebab/paris-d54.html"

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all articles
articles = soup.find_all('article')

# Limiting to 20 restaurants
restaurants_count = 0

# Iterate through each article and extract restaurant information
for article in articles:
    if restaurants_count >= 20:
        break

    # Extract the name
    name = article.find('h3').text.strip()

    # Extract the address
    address = article.find('p').text.strip()

    # Extract the rating
    rating = int(article.find('div', class_='stars').attrs['class'][1][1:])

    # Print restaurant information
    print("Name:", name)
    print("Address:", address)
    print("Rating:", rating)
    print()

    restaurants_count += 1
