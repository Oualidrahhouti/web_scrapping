import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fonction pour extraire les données du tableau d'une page Wikipedia
def extract_table_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {"class": "wikitable"})
    rows = table.find_all('tr')
    data = {}
    for row in rows[1:]:  # Ignorer la ligne d'en-tête
        columns = row.find_all(['th', 'td'])
        country = columns[0].get_text().strip()
        data[country] = [col.get_text().strip() for col in columns[1:]]
    return data

# URLs des pages Wikipedia
url1 = "https://en.wikipedia.org/wiki/Epidemiology_of_depression"
url2 = "https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration"

# Extraire les données des deux tableaux
table1_data = extract_table_data(url1)
table2_data = extract_table_data(url2)

# Fusionner les données des deux tableaux
combined_data = {}
for country in table1_data.keys():
    if country in table2_data:
        combined_data[country] = table1_data[country] + table2_data[country]

# Nettoyer les données et fusionner dans un DataFrame
cleaned_data = []
for country, values in combined_data.items():
    sunshine_values = []
    for value in values[1:]:  # Commencer à partir de l'index 1 pour éviter le nom du pays
        try:
            sunshine_values.append(float(value))
        except ValueError:
            sunshine_values.append(0)
    # Ajouter les données nettoyées au DataFrame
    cleaned_data.append([country] + sunshine_values)

# Créer un DataFrame
columns = ['Country'] + ['Value_' + str(i) for i in range(1, len(cleaned_data[0]))]
df = pd.DataFrame(cleaned_data, columns=columns)

# Afficher la corrélation à l'aide d'un scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Value_1', y='Value_2')
plt.title('Corrélation entre les deux variables')
plt.xlabel('depressed people')
plt.ylabel('sunshine hours')
plt.show()
