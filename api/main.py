from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/conjuguer', methods=['GET'])
def conjuguer():
    # Récupérer le verbe depuis les paramètres de requête
    verbe = request.args.get('verbe')
    
    # Vérifier si un verbe a été fourni
    if not verbe:
        return jsonify({"error": "Veuillez fournir un verbe dans l'URL, par exemple ?verbe=faire"}), 400
    
    # URL pour le scraping du verbe
    url = f"https://leconjugueur.lefigaro.fr/conjugaison/verbe/{verbe}.html"
    
    # Récupérer le contenu de la page
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": f"Impossible de récupérer les données pour le verbe '{verbe}'"}), 500
    
    # Parser le contenu HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire les modes et temps de conjugaison
    modes_temps = []
    for conjugBloc in soup.find_all('div', class_='conjugBloc'):
        mode_temps = conjugBloc.find('div', class_='tempsBloc').text.strip()
        conjugaison = []

        # Trouver les lignes de conjugaison
        for line in conjugBloc.find_all('b'):
            text = line.text.strip()
            # Ignorer les lignes vides ou incorrectes
            if text and text != 'f':  # pour ignorer les tronçons comme 'f'
                conjugaison.append(text)

        # Correction des morceaux fragmentés
        conjugaison = ["".join(conjugaison[i:i+2]) for i in range(0, len(conjugaison), 2)]

        # Ajouter au résultat final si la conjugaison est non vide
        if conjugaison:
            modes_temps.append({
                "mode_temps": mode_temps,
                "conjugaison": conjugaison
            })
    
    return jsonify(modes_temps)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
