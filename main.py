from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Fonction pour analyser la page web et extraire les conjugaisons
def extract_conjugations_from_url(verbe):
    # URL dynamique basée sur le verbe fourni
    url = f'https://leconjugueur.lefigaro.fr/conjugaison/verbe/{verbe}.html'
    
    # Envoyer une requête GET pour récupérer la page HTML
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        conjugations = []

        # Trouver tous les blocs de conjugaison (bloc de temps de conjugaison)
        conjug_blocks = soup.find_all('div', class_='conjugBloc')

        # Pour chaque bloc de conjugaison
        for block in conjug_blocks:
            mode_temps_elem = block.find('div', class_='tempsBloc')
            if mode_temps_elem:
                mode_temps = mode_temps_elem.text.strip()  # Ex: "Présent", "Passé composé", etc.
                
                # Trouver toutes les conjugaisons dans ce bloc
                conjugaison_lines = []
                for conjug_line in block.find_all('li'):
                    # Nettoyer chaque ligne de conjugaison
                    conjugaison_lines.append(conjug_line.text.strip())

                # Ajouter au résultat
                if conjugaison_lines:
                    conjugations.append({
                        "mode_temps": mode_temps,
                        "conjugaison": conjugaison_lines
                    })

        return conjugations
    else:
        return {"error": f"Impossible de récupérer les données pour le verbe '{verbe}'."}

@app.route('/conjuguer', methods=['GET'])
def conjuguer():
    # Récupérer le verbe depuis les paramètres de la requête
    verbe = request.args.get('verbe')
    
    # Vérifier si un verbe a été fourni
    if not verbe:
        return jsonify({"error": "Veuillez fournir un verbe dans l'URL, par exemple ?verbe=faire"}), 400
    
    # Extraire les conjugaisons pour ce verbe
    conjugations = extract_conjugations_from_url(verbe)
    
    return jsonify(conjugations)

if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(host='0.0.0.0', port=5000)
