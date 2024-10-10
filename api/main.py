from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/modes', methods=['GET'])
def get_modes():
    url = "https://leconjugueur.lefigaro.fr/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver tous les modes
    modes = soup.find_all('h2', class_='modeBloc')

    # Extraire les informations
    liste_modes = []
    for mode in modes:
        nom_mode = mode.find('a').text.strip()
        lien_mode = mode.find('a')['href']
        liste_modes.append({
            'nom': nom_mode,
            'lien': lien_mode
        })

    return jsonify(liste_modes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
