from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# URL de la page du conjugueur
url = 'https://leconjugueur.lefigaro.fr/conjugaison/verbe/faire.html'

# Fonction pour analyser la page web et extraire les conjugaisons
def extract_conjugations_from_url(url):
    # Envoyer une requête GET pour récupérer la page HTML
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        conjugations = []

        # Trouver tous les blocs de conjugaison
        conjug_blocks = soup.find_all('div', class_='tempsBloc')

        for block in conjug_blocks:
            mode_temps = block.text.strip()  # Le nom du mode et du temps (ex: "Présent", "Passé composé", etc.)
            conjugaison_block = block.find_next('div')  # Trouver le bloc suivant qui contient les conjugaisons
            conjugaisons = [line.strip() for line in conjugaison_block.stripped_strings]  # Extraire les conjugaisons

            conjugations.append({
                "mode_temps": mode_temps,
                "conjugaison": conjugaisons
            })
        return conjugations
    else:
        return {"error": "Impossible de récupérer les données."}

@app.route('/')
def home():
    # Appeler la fonction pour extraire les conjugaisons
    conjugations = extract_conjugations_from_url(url)
    return jsonify(conjugations)

if __name__ == '__main__':
    # Lancer l'application Flask sur l'hôte 0.0.0.0 et le port 5000
    app.run(host='0.0.0.0', port=5000)
    
