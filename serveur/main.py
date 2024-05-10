import socket
import sqlite3
import threading


# Créer un socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

def handle_client(client_socket):
    while True:
        # Recevoir la requête du client
        request = client_socket.recv(1024).decode()
        print("Requête reçue:", request)
        # Exécuter la fonction correspondante et récupérer les résultats
        parts = request.split(';')
        print("Part 1:", parts[0])
        if len(parts) != 2:
            print("Requête invalide")
            break
        print("Part 2:", parts[1])
        function_name, args = parts
        args = args.split(',')
        if function_name == 'ajouter_livreur_bdd':
            ajouter_livreur_bdd(*args)
        elif function_name == 'get_id_localisation':
            get_id_localisation(*args)
        elif function_name == 'afficher_colonnes_table':
            afficher_colonnes_table(*args)
        elif function_name == 'recuperer_missions':
            recuperer_missions(*args)
        elif function_name == 'existe_dans_base':
            existe_dans_base(*args)
        elif function_name == 'update_mission':
            update_mission(*args)
        elif function_name == 'update_livreur':
            update_livreur(*args)
        elif function_name == 'inserer_mission':
            inserer_mission(*args)

    client_socket.close()

def existe_dans_base(*args):
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    print(args)
    cursor.execute(args[0])
    results = cursor.fetchall()
    # Envoyer les résultats au client
    client_socket.send(str(results).encode())
    conn.close()

def ajouter_livreur_bdd(*args):
    nom, prenom, statut_livreur, capacite, autonomie, etat, id_localisation = args[0], args[1], args[2], args[3], args[4], args[5], args[6]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    # Requête SQL pour insérer un livreur dans la table Livreur
    cursor.execute("INSERT INTO camion (capacite, autonomie, etat) VALUES (?,?,?)", (capacite, autonomie, etat))
    conn.commit()
    print("Camion ajouté à la base de données")
    id_camion = cursor.lastrowid
    cursor.execute("INSERT INTO livreur VALUES (?,?,?,?,?)", (nom, prenom, statut_livreur, id_camion, id_localisation))
    conn.commit()
    print("Livreur ajouté à la base de données")
    conn.close()

def get_id_localisation(*args):
    longi, lattitude = args[0], args[1]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_localisation FROM localisation WHERE longitude = ? AND latitude = ?", (float(longi), float(lattitude)))
    row = cursor.fetchone()
    if row is not None:
        conn.close()
        result = row[0]
    else:
        cursor.execute("INSERT INTO localisation (longitude, latitude) VALUES (?,?)", (float(longi), float(lattitude)))
        conn.commit()
        conn.close()
        result =  cursor.lastrowid
    # Envoyer le résultat au client
    client_socket.send(str(result).encode())

def afficher_colonnes_table(*args):
    nom_table = args[0]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()

    # Exécute la requête pour récupérer les informations sur la table
    cursor.execute("PRAGMA table_info({})".format(nom_table))

    # Récupère les résultats de la requête
    results = cursor.fetchall()

    # Affiche les noms des colonnes
    print("Colonnes de la table {}:".format(nom_table))
    for row in results:
        print(row[1])  # La colonne "name" contient le nom de la colonne

    # Ferme la connexion
    conn.close()

def recuperer_missions(*args):
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_message FROM mission")
    results = cursor.fetchall()
    # Envoyer les résultats au client
    client_socket.send(str(results).encode())
    # Ferme la connexion
    conn.close()

def update_mission(*args):
    id_livreur, etat, id_message = args[0], args[1], args[2]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE mission SET id_livreur = ?, etat = ? WHERE id_message = ?", (id_livreur, etat, id_message))
    conn.commit()
    conn.close()

def update_livreur(*args):
    nom, prenom, id_localisation, capacite, autonomie, etat, id_livreur = args[0], args[1], args[2], args[3], args[4], args[5], args[6]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE camion SET capacite = ?, autonomie = ?, etat = ? WHERE id_camion = ?", (capacite, autonomie, etat, id_livreur))
    conn.commit()
    cursor.execute("UPDATE livreur SET nom = ?, prenom = ?, id_localisation = ?, id_camion = ? WHERE id_livreur = ?", (nom, prenom, id_localisation, capacite, autonomie, etat, id_livreur))
    conn.commit()
    conn.close()

def inserer_mission(*args):
    etat, details, quantite, salaire, date_envoie, date_limite, id_livreur, id_localisation_d, id_localisation_a = args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8]
    conn = sqlite3.connect('projet.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mission (etat, details, quantite, salaire, date_envoie, date_limite, id_livreur, id_localisation_depart, id_localisation_arrivee) VALUES (?,?,?,?,?,?,?,?,?)", (etat, details, quantite, salaire, date_envoie, date_limite, id_livreur, id_localisation_d, id_localisation_a))
    conn.commit()
    conn.close()

while True:
    # Accepter une connexion client
    client_socket, addr = server_socket.accept()

    # Créer un nouveau thread pour gérer la connexion
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()