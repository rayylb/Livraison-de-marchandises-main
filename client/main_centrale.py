import tkinter as tk
from tkinter import Tk, Canvas, PhotoImage
from tkinter import messagebox
from datetime import datetime
from class_projet import *
import sqlite3
import geopy,certifi,ssl
from geopy.geocoders import Nominatim
from fonctions import *
import folium


def valider_ajout(entry_details, entry_quantite, entry_salaire, entry_date_limite, entry_loc, ajout_window):

    # Fonction pour valider l'ajout de la mission
    details = entry_details.get()
    quantite_str = entry_quantite.get()
    salaire_str = entry_salaire.get()
    date_limite_str = entry_date_limite.get()
    adresse = entry_loc.get()

    # Vérifier les entrées et afficher une boîte de dialogue en cas d'erreur
    if not details or not quantite_str or not salaire_str or not date_limite_str:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
        return

    try:
        quantite = int(quantite_str)
        salaire = float(salaire_str)
        date_limite = datetime.strptime(date_limite_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Erreur", "Veuillez saisir des valeurs numériques valides pour la quantité et le salaire, et respecter le format de date (YYYY-MM-DD) pour la date limite.")
        return

    #convertir l'adresse en coordonnées
    longitude, latitude = coordonnees_from_adresse(adresse)

    #ajout de la localisation à la base de donnéees et get de son id
    id_localisation = get_id_localisation(longitude, latitude)

    # Ajouter la mission à la liste de missions dans la base de données)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'inserer_mission;{0},{details},{quantite},{salaire},{datetime.now()},{date_limite},{0}, {0}, {id_localisation}'
    print(request)
    client_socket.send(request.encode())
    client_socket.close()
    ajout_window.destroy()
    messagebox.showinfo("Mission ajoutée", "La mission a été ajoutée avec succès.")

def afficher_missions(missions_list):
    affichage_window = tk.Toplevel()
    affichage_window.title("Missions")

    # Créer un widget Listbox pour afficher les missions
    listbox_missions = tk.Listbox(affichage_window, height=10, width=50)
    listbox_missions.pack(padx=10, pady=10)

    # Ajouter les détails des missions à la Listbox
    for mission in missions_list:
        mission_details = f"Mission {mission.id}: {mission.details}"
        listbox_missions.insert(tk.END, mission_details)

    # Lier le double-clic sur une mission à l'affichage de ses détails
    listbox_missions.bind("<Double-Button-1>", lambda event: afficher_details_mission(missions_list[listbox_missions.curselection()[0]]))

affichage_window = None  # Déclarer la variable en dehors des fonctions

def afficher_dernieres_missions():
    global affichage_window  # Utiliser la variable globale dans la fonction
    # Fonction pour afficher les 10 dernières missions dans une fenêtre Tkinter
    missions = recuperer_missions()
    top_10_missions = missions[-10:]  # Récupérer les 10 dernières missions
    
    affichage_window = tk.Toplevel()
    affichage_window.title("Dernières Missions")

    # Cadre pour contenir les boutons
    cadre_boutons = tk.Frame(affichage_window)
    cadre_boutons.pack(pady=5)

    # # Ajouter un bouton pour afficher les missions non pourvues
    # button_missions_non_pourvues = tk.Button(cadre_boutons, text="Afficher les missions non pourvues", command=afficher_missions_non_pourvues)
    # button_missions_non_pourvues.pack(side=tk.LEFT, padx=5)

    # # Ajouter un bouton pour afficher toutes les missions
    # button_afficher_toutes_les_missions = tk.Button(cadre_boutons, text="Afficher toutes les missions", command=afficher_toutes_les_missions)
    # button_afficher_toutes_les_missions.pack(side=tk.LEFT, padx=5)

    # Créer un widget Listbox pour afficher les missions
    listbox_missions = tk.Listbox(affichage_window, height=10, width=50)
    listbox_missions.pack(padx=10, pady=10)

    # Ajouter les détails des missions à la Listbox
    for mission in top_10_missions:
        mission_details = f"Mission {mission.id}: {mission.details}"
        listbox_missions.insert(tk.END, mission_details)

    # Lier le double-clic sur une mission à l'affichage de ses détails
    listbox_missions.bind("<Double-Button-1>", lambda event: afficher_details_mission(top_10_missions[listbox_missions.curselection()[0]]))

# def afficher_missions_non_pourvues():
#     missions_non_pourvues = [mission for mission in missions if mission.etat != "Pourvue"]
#     affichage_window.destroy()  # Fermer la fenêtre actuelle
#     afficher_missions(missions_non_pourvues)

# def afficher_toutes_les_missions():
#     affichage_window.destroy()  # Fermer la fenêtre actuelle
#     afficher_missions(missions)

def afficher_details_mission(mission):
    details_window = tk.Toplevel()
    details_window.title(f"Détails Mission {mission.id}")

    # Afficher les informations de la mission
    label_id = tk.Label(details_window, text=f"ID: {mission.id}")
    label_id.grid(row=1, column=0, sticky="w")

    label_etat = tk.Label(details_window, text=f"État: {mission.etat}")
    label_etat.grid(row=2, column=0, sticky="w")

    label_details = tk.Label(details_window, text=f"Détails: {mission.details}")
    label_details.grid(row=3, column=0, sticky="w")

    label_quantite = tk.Label(details_window, text=f"Quantité: {mission.quantite}")
    label_quantite.grid(row=4, column=0, sticky="w")

    label_salaire = tk.Label(details_window, text=f"Salaire: {mission.salaire}")
    label_salaire.grid(row=5, column=0, sticky="w")

    label_date_limite = tk.Label(details_window, text=f"Date limite: {mission.date_limite}")
    label_date_limite.grid(row=6, column=0, sticky="w")
    print(mission.id_localisation_a)
    loc = Localisation(mission.id_localisation_a)

    label_id_localisation_a = tk.Label(details_window, text=f"Localisation d'arrivée: {loc.adresse}")
    label_id_localisation_a.grid(row=7, column=0, sticky="w")

    # Bouton pour supprimer la mission
    button_supprimer = tk.Button(details_window, text="Supprimer", command=lambda: supprimer_mission(mission.id, details_window))
    button_supprimer.grid(row=8, column=0, pady=10)

    # Affichez la fenêtre
    details_window.mainloop()

def supprimer_mission(id, details_window):
    # Fonction pour supprimer une mission
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'supprimer_mission;{id}'
    client_socket.send(request.encode())
    client_socket.close()
    details_window.destroy()
    messagebox.showinfo("Mission supprimée", "La mission a été supprimée avec succès.")

def recuperer_livreurs():
    # Fonction pour récupérer la liste des livreurs depuis la base de données
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = 'recuperer_livreurs;'
    client_socket.send(request.encode())
    results = client_socket.recv(1024).decode()[1:-1]
    print(results)
    client_socket.close()

    # Créer une liste de livreurs à partir des résultats
    livreurs = []
    nombres = []

    # Parcours de la chaîne de caractères
    nombre_actuel = ''
    for caractere in results:
        if caractere.isdigit():  # Vérifie si le caractère est un chiffre
            nombre_actuel += caractere
        elif nombre_actuel:  # Si nous avons accumulé un nombre
            nombres.append(nombre_actuel)
            nombre_actuel = ''

    for id in nombres:
        if id:
            print(id)
            livreur = Livreur(id)
            livreurs.append(livreur)

    return livreurs

# Fonction pour ouvrir la fenêtre d'ajout de mission
def ouvrir_ajout_window():
    ajout_window = tk.Toplevel()
    ajout_window.title("Ajouter Mission")

    # Widgets pour le formulaire
    label_details = tk.Label(ajout_window, text="Détails de la mission:")
    label_details.pack()
    entry_details = tk.Entry(ajout_window)
    entry_details.pack()

    label_quantite = tk.Label(ajout_window, text="Quantité:")
    label_quantite.pack()
    entry_quantite = tk.Entry(ajout_window)
    entry_quantite.pack()

    label_salaire = tk.Label(ajout_window, text="Salaire:")
    label_salaire.pack()
    entry_salaire = tk.Entry(ajout_window)
    entry_salaire.pack()

    label_date_limite = tk.Label(ajout_window, text="Date limite (YYYY-MM-DD):")
    label_date_limite.pack()
    entry_date_limite = tk.Entry(ajout_window)
    entry_date_limite.pack()

    label_loc = tk.Label(ajout_window, text="Adresse de livraison:")
    label_loc.pack()
    entry_loc = tk.Entry(ajout_window)
    entry_loc.pack()

    button_valider = tk.Button(ajout_window, text="Valider", command=lambda: valider_ajout(entry_details, entry_quantite, entry_salaire, entry_date_limite, entry_loc, ajout_window))
    button_valider.pack()

def ajouter_livreur():
    ajout_livreur_window = tk.Toplevel()
    ajout_livreur_window.title("Ajouter Livreur")

    # Widgets pour le formulaire
    label_nom = tk.Label(ajout_livreur_window, text="Nom:")
    label_nom.pack()
    entry_nom = tk.Entry(ajout_livreur_window)
    entry_nom.pack()

    label_prenom = tk.Label(ajout_livreur_window, text="Prénom:")
    label_prenom.pack()
    entry_prenom = tk.Entry(ajout_livreur_window)
    entry_prenom.pack()

    label_adresse = tk.Label(ajout_livreur_window, text="Adresse:")
    label_adresse.pack()
    entry_adresse = tk.Entry(ajout_livreur_window)
    entry_adresse.pack()

    label_capacite_camion = tk.Label(ajout_livreur_window, text="Capacité du camion:")
    label_capacite_camion.pack()
    entry_capacite_camion = tk.Entry(ajout_livreur_window)
    entry_capacite_camion.pack()

    label_autonomie_camion = tk.Label(ajout_livreur_window, text="Autonomie du camion:")
    label_autonomie_camion.pack()
    entry_autonomie_camion = tk.Entry(ajout_livreur_window)
    entry_autonomie_camion.pack()

    label_etat_camion = tk.Label(ajout_livreur_window, text="État du camion:")
    label_etat_camion.pack()
    entry_etat_camion = tk.Entry(ajout_livreur_window)
    entry_etat_camion.pack()

    label_mdp = tk.Label(ajout_livreur_window, text="Mot de passe:")
    label_mdp.pack()
    entry_mdp = tk.Entry(ajout_livreur_window)
    entry_mdp.pack()

    button_valider = tk.Button(ajout_livreur_window, text="Valider", command=lambda: valider_ajout_livreur(entry_nom, entry_prenom, entry_adresse, entry_capacite_camion, entry_autonomie_camion, entry_etat_camion, entry_mdp, ajout_livreur_window))
    button_valider.pack()

def valider_ajout_livreur(entry_nom, entry_prenom, entry_adresse, entry_capacite_camion, entry_autonomie_camion, entry_etat_camion, mdp, ajout_livreur_window):
    # Fonction pour valider l'ajout du livreur
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    adresse = entry_adresse.get()
    capacite_camion_str = entry_capacite_camion.get()
    autonomie_camion_str = entry_autonomie_camion.get()
    etat_camion = entry_etat_camion.get()
    mdp = mdp.get()

    # Vérifier les entrées et afficher une boîte de dialogue en cas d'erreur
    if not nom or not prenom or not adresse or not capacite_camion_str or not autonomie_camion_str or not etat_camion or not mdp:
        messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
        return
    
        #convertir l'adresse en coordonnées
    longitude, latitude = coordonnees_from_adresse(adresse)

    #ajout de la localisation à la base de donnéees et get de son id
    id_localisation = get_id_localisation(longitude, latitude)

    # Ajouter le livreur à la liste de livreurs dans la base de données
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    request = f'inserer_livreur;{nom},{prenom},{id_localisation},{capacite_camion_str},{autonomie_camion_str},{etat_camion},{mdp}'
    client_socket.send(request.encode())
    rep = client_socket.recv(1024).decode()
    client_socket.close()
    ajout_livreur_window.destroy()
    messagebox.showinfo(f'Livreur ajouté', f'Le livreur a été ajouté avec succès. {rep}')

def afficher_livreurs():
    livreurs = recuperer_livreurs()
    afficher_livreurs_window = tk.Toplevel()
    afficher_livreurs_window.title("Livreurs")

    # Créer un widget Listbox pour afficher les livreurs
    listbox_livreurs = tk.Listbox(afficher_livreurs_window, height=10, width=50)
    listbox_livreurs.pack(padx=10, pady=10)

    # Ajouter les détails des livreurs à la Listbox
    for livreur in livreurs:
        livreur_details = f"Livreur {livreur.id}: {livreur.nom} {livreur.prenom}"
        listbox_livreurs.insert(tk.END, livreur_details)

    # Lier le double-clic sur un livreur à l'affichage de ses détails
    listbox_livreurs.bind("<Double-Button-1>", lambda event: afficher_details_livreur(livreurs[listbox_livreurs.curselection()[0]]))

def afficher_details_livreur(livreur):
    details_window = tk.Toplevel()
    details_window.title(f"Détails Livreur {livreur.id}")

    # Afficher les informations du livreur
    label_id = tk.Label(details_window, text=f"ID: {livreur.id}")
    label_id.grid(row=1, column=0, sticky="w")

    label_nom = tk.Label(details_window, text=f"Nom: {livreur.nom}")
    label_nom.grid(row=2, column=0, sticky="w")

    label_prenom = tk.Label(details_window, text=f"Prénom: {livreur.prenom}")
    label_prenom.grid(row=3, column=0, sticky="w")

    label_adresse = tk.Label(details_window, text=f"Adresse: {Localisation(livreur.id_localisation).adresse}")
    label_adresse.grid(row=4, column=0, sticky="w")

    c = Camion(livreur.id_camion)
    label_capacite_camion = tk.Label(details_window, text=f"Capacité du camion: {c.capacite}")
    label_capacite_camion.grid(row=5, column=0, sticky="w")

    label_autonomie_camion = tk.Label(details_window, text=f"Autonomie du camion: {c.autonomie}")
    label_autonomie_camion.grid(row=6, column=0, sticky="w")

    label_etat_camion = tk.Label(details_window, text=f"État du camion: {c.etat}")
    label_etat_camion.grid(row=7, column=0, sticky="w")


# Créer une fenêtre principale
root = tk.Tk()
root.title("Centrale de Livraison")

# Bouton pour afficher les 10 dernières missions
button_afficher_missions = tk.Button(root, text="Afficher les missions", command=afficher_dernieres_missions)
button_afficher_missions.pack(padx = 10, pady=10)

# Bouton pour ajouter une mission
button_ajouter_mission = tk.Button(root, text="Ajouter une mission", command=ouvrir_ajout_window)
button_ajouter_mission.pack(padx=10, pady=10)

button_afficher_livreurs = tk.Button(root, text="Afficher les livreurs", command=afficher_livreurs)
button_afficher_livreurs.pack(padx=10, pady=10)

button_ajouter_livreur = tk.Button(root, text="Ajouter un livreur", command=ajouter_livreur)
button_ajouter_livreur.pack(padx=10, pady=10)

# Fonction pour afficher les messages d'erreur de manière modale
def show_modal_error(title, message):
    modal = tk.Toplevel()
    modal.grab_set()  # Rendre la fenêtre modale, bloque l'accès aux autres fenêtres
    modal.title(title)
    tk.Label(modal, text=message).pack(padx=20, pady=10)
    tk.Button(modal, text="OK", command=modal.destroy).pack(pady=5)

# Rediriger les messages d'erreur vers les fenêtres modales
def show_error(title, message):
    show_modal_error(title, message)


messagebox.showerror = show_error

# Lancer la boucle principale Tkinter
root.mainloop()
