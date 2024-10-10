import requests
from bs4 import BeautifulSoup

url = "https://leconjugueur.lefigaro.fr/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver tous les verbes
# Cela dépend de la structure HTML du site, vous devrez peut-être ajuster les sélecteurs
verbes = soup.find_all('a', class_='verbe')

# Extraire les verbes
liste_verbes = [verbe.text for verbe in verbes]

# Afficher la liste des verbes
for verbe in liste_verbes:
    print(verbe)
  
