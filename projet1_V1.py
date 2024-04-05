import requests

# Fonction pour vérifier si la valeur est un code postal valide
def est_code_postal(val):
    # Vérifie si val est une chaîne de caractères et ne contient que des chiffres
    if isinstance(val, str) and val.isdigit():
        # Vérifie si égale à 5 ou 2
        if len(val) == 5 or len(val) == 2:
            return True  # Valide si bon
    return False  # Renvoie False si pas bon

def verification_api():
    try:
        url = input("Lien d'une API : ")  # Saisir l'url
        response = requests.get(url)  # Requête get du lien
        data = response.json()  # Convertit en  JSON
        print("Lancement de la recherche de département ")
    except:
        # Erreur en cas de mauvais lien
        print("========================================================")
        print("le lien n'est pas bon ")
        print("Merci de mettre un lien correcte")
        print("========================================================")
        return verification_api()  # Rappelle la fonction pour permettre à l'utilisateur de saisir à nouveau l'URL
    departement(data)  # Appel la fonction

# Fonction pour rechercher le département ou le code postal dans les données de l'API
def departement(data):
    while True:  # Boucle jusqu'à ce que les données valides soient saisies ou qu'une erreur survienne
        try:
            num = input("Veuillez entrer un département ou un code postal : ")
            if not est_code_postal(num):  # Vérifie si la saisie de l'utilisateur est un code postal valide
                print("Le département ou le code postal doit être une chaîne de 2 ou 5 chiffres.")
                continue  # Passe à la suite s i c'est bon
            liste_population = []  # table qui vas stocker la population
            print(f"Tentative avec le département ou code postal : {num} ")
            print("========================================================")

            for element in data:  # Chaque élements des données de l'api
                if element["codeDepartement"] == num:  # Vérifie si le code département selectionner existe
                    liste_population.append(element["population"])  # Si oui ajoute la/les populations en lien avec le Departement
                elif num in element["codesPostaux"]:  # Vérifie si le code postal selectionner existe
                    liste_population.append(element["population"])

            print(f"Il y a {sum(liste_population)} habitant(e)s.")  # Affiche le nb total de population
            break  # Sort de la boucle si il n'y pas eu d'erreur
        except Exception as e:
            # Gère les exceptions en cas d'erreur lors du traitement des données de l'API
            print(f"Une erreur s'est produite : {e}. Veuillez réessayer.")

# Appel de la fonction principale pour démarrer le programme
verification_api()
