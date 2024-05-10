import sqlite3
from datetime import datetime
import geopy,certifi,ssl
from geopy.geocoders import Nominatim
import socket

class Message:

    def __init__(self, id):
        self.id = id
        self.contenu = ""
        self.date_envoie = "" 
        self.id_livreur = ""
        self.id_centrale = ""
        self.id_mission = ""
    
    def setContenu(self, contenu):  #self represente un message particulier 
        self.contenu = contenu       # ici contenu d'un message en particulier
    
    def envoyer(self, date, contenu, id_livreur, id_centrale, id_mission):
        global cursor
        cursor.execute(
            "INSERT INTO message (contenu, date_envoie, id_mission, id_livreur, id_centrale) \
            VALUES (?, ?, ?, ?, ?)", (contenu, date, id_mission, id_livreur, id_centrale)
        )
        
        print("Message envoyé")

class Livreur:
    def __init__(self, id):
        self.id = id
        self.nom = ""
        self.prenom = ""
        self.statut_livreur = True
        self.id_camion = ""
        self.id_localisation = ""
        
        # Vérifier si l'ID existe dans la base de données et initialiser les attributs
        self.existe_dans_base()

    def existe_dans_base(self):
        # Créer un socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Envoyer une requête SQL au serveur
        sql_query = f"existe_dans_base; SELECT * FROM livreur WHERE id_livreur = {self.id}"
        client_socket.send(sql_query.encode())

        # Recevoir les résultats du serveur
        results = client_socket.recv(1024).decode()

        # Fermer le socket client
        client_socket.close()

        # Vérifier si une ligne a été retournée par la requête
        if results:
            # Assigner les valeurs de la base de données aux attributs de l'objet Livreur
            row = results.split(',')
            self.nom = row[1]
            self.prenom = row[2]
            self.statut_livreur = row[3]
            self.id_camion = row[4]
            self.id_localisation = row[5][1]
        else:
            raise ValueError("Aucun livreur avec cet ID trouvé dans la base de données")
        
    def est_volontaire(self):
        return self.statut_livreur and self.id_camion != ""
    
    def afficher_informations(self):
        return f"Nom: {self.nom}\nPrénom: {self.prenom}\nStatut: {self.statut_livreur}\nID localisation: {self.id_localisation}"

        
class Centrale:

    def __init__(self, id):
        self.id = id
        self.nom = ""
        self.id_localisation = ""
        self.missions = []  

    def ajouter_mission(self,mission):
        self.missions.append(mission)

    def attribuer_mission(self,livreur,mission):
        if livreur.est_volontaire():
            livreur.ajouter_mission(mission)
            self.ajouter_mission(mission)
    
    def repondre_aux_messages(self):
        pass
        


class Camion:

    def __init__(self, id):
        self.id = id
        self.autonomie = 0
        self.capacite = 0
        self.etat = ""
        
        # Vérifier si l'ID existe dans la base de données et initialiser les attributs
        self.existe_dans_base()

    def existe_dans_base(self):
        # Créer un socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Envoyer une requête SQL au serveur
        sql_query = f"existe_dans_base; SELECT * FROM camion WHERE id_camion = {self.id}"
        client_socket.send(sql_query.encode())

        # Recevoir les résultats du serveur
        results = client_socket.recv(1024).decode()

        # Fermer le socket client
        client_socket.close()

        # Vérifier si une ligne a été retournée par la requête
        if results:
            # Assigner les valeurs de la base de données aux attributs de l'objet Camion
            row = results.split(',')
            self.capacite = row[1]
            self.autonomie = row[2]
            self.etat = row[3][:-2]
        else:
            raise ValueError("Aucun camion avec cet ID trouvé dans la base de données")
        
class Mission:

    def __init__(self, id):
        self.id = id
        self.etat = False
        self.details = ""
        self.quantite = 0
        self.salaire = 0
        self.date_envoie = ""
        self.date_limite = ""
        self.id_livreur = ""
        self.id_localisation_d = ""
        self.id_localisation_a = ""
        self.existe_dans_base()

    def existe_dans_base(self):
        # Créer un socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Envoyer une requête SQL au serveur
        sql_query = f"existe_dans_base; SELECT * FROM mission WHERE id_message = {self.id}"
        client_socket.send(sql_query.encode())

        # Recevoir les résultats du serveur
        results = client_socket.recv(1024).decode()

        # Fermer le socket client
        client_socket.close()

        if results:
            row = results.split(',')
            self.etat = row[1]
            self.details = row[2]
            self.quantite = row[3]
            self.salaire = row[4]
            self.date_envoie = row[5]
            self.date_limite = row[6]
            self.id_livreur = row[7]
            self.id_localisation_d = row[8]
            self.id_localisation_a = row[9][1]

class Localisation:

    def __init__(self, id):
        self.id = int(id)
        self.longitude = 0
        self.latitude = 0
        self.adresse = ""
        self.existe_dans_base()
        self.get_adresse()

    def existe_dans_base(self):
        # Créer un socket client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Envoyer une requête SQL au serveur
        sql_query = f"existe_dans_base; SELECT * FROM localisation WHERE id_localisation = {self.id}"
        client_socket.send(sql_query.encode())

        # Recevoir les résultats du serveur
        results = client_socket.recv(1024).decode()

        # Fermer le socket client
        client_socket.close()

        if results:
            row = results.split(',')
            self.longitude = float(row[1])
            self.latitude = float(row[2][1:-2])
        else:
            raise ValueError("Aucune localisation avec cet ID trouvé dans la base de données")
    
    def get_adresse(self):
        print(self.longitude, self.latitude)
        geopy.geocoders.options.default_ssl_context = ssl.create_default_context(cafile=certifi.where())
        geolocator = Nominatim(user_agent="projet")
        location = geolocator.reverse((self.longitude, self.latitude))
        self.adresse = location.address