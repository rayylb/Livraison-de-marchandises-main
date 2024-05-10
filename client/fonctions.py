import socket
import ssl
import certifi
import geopy
from geopy.geocoders import Nominatim
import ast
from class_projet import *

def ajouter_livreur_bdd(nom, prenom, statut_livreur, capacite, autonomie, etat, id_localisation):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'ajouter_livreur_bdd;{nom},{prenom},{statut_livreur},{capacite},{autonomie},{etat},{id_localisation}'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    print(response)

def coordonnees_from_adresse(adresse):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(adresse)
    return location.latitude, location.longitude

def get_id_localisation(longitude, latitude):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'get_id_localisation;{longitude},{latitude}'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

def afficher_colonnes_table(table_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'afficher_colonnes_table;{table_name}'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    client_socket.close()

def recuperer_missions():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'recuperer_missions;'
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()
    missions = ast.literal_eval(response)
    return [Mission(*mission) for mission in missions]
    client_socket.close()
