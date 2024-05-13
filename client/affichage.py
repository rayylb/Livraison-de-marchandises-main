import tkinter as tk
from tkinter import messagebox
import sqlite3
from class_projet import *
from fonctions import *
import webbrowser
import global_var
from tkcalendar import Calendar

# Fonction pour afficher les informations du livreur et les 10 dernières missions dans une seule fenêtre
def afficher_informations(livreur):
    missions = recuperer_missions()[-10:]  # Récupérer les 10 dernières missions
    
    fenetre_info = tk.Toplevel()
    fenetre_info.title("Informations Livreur et Missions")

    # Cadre pour les informations du livreur
    cadre_livreur = tk.Frame(fenetre_info)
    cadre_livreur.pack(pady=10)

    # Affichage des informations du livreur dans le cadre
    informations_livreur_label = tk.Label(cadre_livreur, text=livreur.afficher_informations(), justify="left")
    informations_livreur_label.pack(side="left", padx=20)

    # Bouton pour modifier les informations du livreur
    bouton_modifier = tk.Button(cadre_livreur, text="Modifier", command=lambda: modifier_informations(livreur, fenetre_info, informations_livreur_label))
    bouton_modifier.pack(side="right", padx=20)

    # Cadre pour les missions
    cadre_missions = tk.Frame(fenetre_info)
    cadre_missions.pack(pady=10)

    # Créer un widget Listbox pour afficher les missions
    listbox_missions = tk.Listbox(cadre_missions, height=10, width=50)
    listbox_missions.pack(padx=10, pady=10)

    # Ajouter les détails des missions à la Listbox
    for mission in missions:
        mission_details = f"Mission {mission.id}: {mission.details}"
        listbox_missions.insert(tk.END, mission_details)

    # Lier le double-clic sur une mission à l'affichage de ses détails
    listbox_missions.bind("<Double-Button-1>", lambda event: afficher_details_mission(missions[listbox_missions.curselection()[0]], fenetre_info))

# Fonction pour afficher les détails d'une mission sélectionnée
# Fonction pour afficher les détails d'une mission sélectionnée
def afficher_details_mission(mission, fenetre_parent):
    details_window = tk.Toplevel(fenetre_parent)
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

    loc = Localisation(mission.id_localisation_a)

    label_id_localisation_a = tk.Label(details_window, text=f"Localisation d'arrivée: {loc.adresse}")
    label_id_localisation_a.grid(row=7, column=0, sticky="w")

    # Bouton pour ouvrir Google Maps avec l'itinéraire vers la mission
    bouton_itineraire = tk.Button(details_window, text="Itinéraire", command=lambda: ouvrir_itineraire(loc.latitude, loc.longitude))
    bouton_itineraire.grid(row=8, column=0, pady=5)

    cal = Calendar(details_window, selectmode='day')
    cal.grid(row=10, column=0, pady=5)

    # Bouton pour candidater à la mission
    bouton_candidater = tk.Button(details_window, text="Candidater", command=lambda: candidater_a_mission(mission, cal.selection_get()))
    bouton_candidater.grid(row=11, column=0, pady=5)

def afficher_details_mission_reservee(mission, fenetre_parent):
    details_window = tk.Toplevel(fenetre_parent)
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

    label_date_livraison = tk.Label(details_window, text=f"Date limite: {mission.date_envoie}")
    label_date_livraison.grid(row=6, column=0, sticky="w")

    loc = Localisation(mission.id_localisation_a)

    label_id_localisation_a = tk.Label(details_window, text=f"Localisation d'arrivée: {loc.adresse}")
    label_id_localisation_a.grid(row=7, column=0, sticky="w")

    # Bouton pour ouvrir Google Maps avec l'itinéraire vers la mission
    bouton_itineraire = tk.Button(details_window, text="Itinéraire", command=lambda: ouvrir_itineraire(loc.latitude, loc.longitude))
    bouton_itineraire.grid(row=8, column=0, pady=5)


# Fonction pour ouvrir Google Maps avec l'itinéraire vers la mission
def ouvrir_itineraire(latitude, longitude):
    # Générer l'URL pour l'itinéraire vers la mission
    url = f"https://www.google.com/maps/dir/?api=1&destination={longitude},{latitude}"

    # Ouvrir Google Maps dans le navigateur par défaut
    webbrowser.open(url)

# Fonction pour permettre au livreur de candidater à la mission
def candidater_a_mission(mission,date):
    # Code pour permettre au livreur de candidater à la mission
    if int(mission.etat) == 0:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        request = f'candidater_mission;{livreur.id}, {mission.id}, {date}'
        client_socket.send(request.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()
        if response == "True":
            tk.messagebox.showinfo("Succès", "Vous avez candidaté à la mission avec succès.")
        else:
            tk.messagebox.showerror("Erreur", "Vous n'avez pas de capacité suffisante pour réaliser la mission à la date donnée.")
    else:
        tk.messagebox.showerror("Erreur", "La mission n'est plus disponible.")


# Fonction pour modifier les informations du livreur
def modifier_informations(livreur, fenetre_parent, informations_livreur_label):
    # Fonction pour valider les modifications
    camion = Camion(livreur.id_camion)
    def valider_modifications():
        try:
            # Effectuer les assertions
            assert len(champ_nom.get()) > 0, "Le nom ne peut pas être vide"
            assert len(champ_prenom.get()) > 0, "Le prénom ne peut pas être vide"
            assert len(champ_adresse.get()) > 0, "L'adresse ne peut pas être vide"
            assert len(champ_capacite.get()) > 0, "La capacité ne peut pas être vide"
            assert len(champ_autonomie.get()) > 0, "L'autonomie ne peut pas être vide"
            assert len(champ_etat.get()) > 0, "L'état ne peut pas être vide"
            longitude, latitude = coordonnees_from_adresse(champ_adresse.get())
            id_localisation = get_id_localisation(longitude, latitude)

            # Mettre à jour les informations du livreur
            livreur.nom = champ_nom.get()
            livreur.prenom = champ_prenom.get()
            livreur.id_localisation = id_localisation
            camion.capacite = champ_capacite.get()
            camion.autonomie = champ_autonomie.get()
            camion.etat = champ_etat.get()
        
            # Mettre à jour les informations dans la base de données
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 12345))
            request = f'update_livreur;{livreur.nom},{livreur.prenom},{livreur.id_localisation},{camion.capacite},{camion.autonomie},{camion.etat},{livreur.id}, {livreur.id_camion}'
            client_socket.send(request.encode())
            client_socket.close()

            # Mettre à jour l'affichage
            informations_livreur_label.config(text=livreur.afficher_informations())

            # Afficher un message de succès
            tk.messagebox.showinfo("Succès", "Les modifications ont été enregistrées avec succès.")
        except AssertionError as e:
            # Afficher un message d'erreur
            tk.messagebox.showerror("Erreur", str(e))


    # Créer une fenêtre pour la modification des informations
    fenetre_modification = tk.Toplevel(fenetre_parent)
    fenetre_modification.title("Modifier Informations")

    # Créer des champs de saisie pour le nom, le prénom, l'adresse et l'ID du camion
    tk.Label(fenetre_modification, text="Nom :").grid(row=0, column=0, sticky="w")
    tk.Label(fenetre_modification, text="Prénom :").grid(row=1, column=0, sticky="w")
    tk.Label(fenetre_modification, text="Adresse :").grid(row=2, column=0, sticky="w")
    tk.Label(fenetre_modification, text="Capacité du camion :").grid(row=3, column=0, sticky="w")
    tk.Label(fenetre_modification, text="Autonomie du camion :").grid(row=4, column=0, sticky="w")   
    tk.Label(fenetre_modification, text="Etat du camion :").grid(row=5, column=0, sticky="w")

    champ_nom = tk.Entry(fenetre_modification)
    champ_nom.grid(row=0, column=1, padx=5, pady=5)
    champ_nom.insert(tk.END, livreur.nom)

    champ_prenom = tk.Entry(fenetre_modification)
    champ_prenom.grid(row=1, column=1, padx=5, pady=5)
    champ_prenom.insert(tk.END, livreur.prenom)

    loc = Localisation(livreur.id_localisation)
    loc.get_adresse()
    champ_adresse = tk.Entry(fenetre_modification)
    champ_adresse.grid(row=2, column=1, padx=5, pady=5)
    champ_adresse.insert(tk.END, loc.adresse)


    champ_capacite = tk.Entry(fenetre_modification)
    champ_capacite.grid(row=3, column=1, padx=5, pady=5)
    champ_capacite.insert(tk.END, camion.capacite)

    champ_autonomie = tk.Entry(fenetre_modification)
    champ_autonomie.grid(row=4, column=1, padx=5, pady=5)
    champ_autonomie.insert(tk.END, camion.autonomie)

    champ_etat = tk.Entry(fenetre_modification)
    champ_etat.grid(row=5, column=1, padx=5, pady=5)
    champ_etat.insert(tk.END, camion.etat)

    # Bouton pour valider les modifications
    bouton_valider = tk.Button(fenetre_modification, text="Valider", command=valider_modifications)
    bouton_valider.grid(row=6, columnspan=2, padx=5, pady=5)

def afficher_mes_missions(livreur):
    fenetre_info = tk.Toplevel()
    fenetre_info.title("Informations Livreur et Missions")
    missions = recuperer_missions_livreur(livreur.id)
    
    # Cadre pour les missions
    cadre_missions = tk.Frame(fenetre_info)
    cadre_missions.pack(pady=10)
    # Créer un widget Listbox pour afficher les missions
    listbox_missions = tk.Listbox(cadre_missions, height=10, width=50)
    listbox_missions.pack(padx=10, pady=10)

    # Ajouter les détails des missions à la Listbox
    for mission in missions:
        mission_details = f"Mission {mission.id}: {mission.details}"
        listbox_missions.insert(tk.END, mission_details)  
    listbox_missions.bind("<Double-Button-1>", lambda event: afficher_details_mission_reservee(missions[listbox_missions.curselection()[0]], fenetre_info))

def choisir_jour(livreur):
    def afficher_missions_jour():
        date = cal.selection_get()
        print(date)
        missions = recuperer_missions_livreur(livreur.id)
        for mission in missions:
            print(mission.date_envoie[3:-1])
            print (mission.date_envoie[3:-1] == str(date))
        missions_jour = [mission for mission in missions if mission.date_envoie[3:-1] == str(date)]
        fenetre_info = tk.Toplevel()
        fenetre_info.title("Informations Livreur et Missions")
        cadre_missions = tk.Frame(fenetre_info)
        cadre_missions.pack(pady=10)
        listbox_missions = tk.Listbox(cadre_missions, height=10, width=50)
        listbox_missions.pack(padx=10, pady=10)
        for mission in missions_jour:
            mission_details = f"Mission {mission.id}: {mission.details}"
            listbox_missions.insert(tk.END, mission_details)
        listbox_missions.bind("<Double-Button-1>", lambda event: afficher_details_mission_reservee(missions_jour[listbox_missions.curselection()[0]], fenetre_info))
        bouton_trajet = tk.Button(fenetre_info, text="Générer trajet Google Maps", command=lambda: generer_trajet_google_maps(missions))
        bouton_trajet.pack(pady=5)
    fenetre_info = tk.Toplevel()
    fenetre_info.title("Choisir une date")
    cal = Calendar(fenetre_info, selectmode='day')
    cal.pack(pady=5)
    bouton_valider = tk.Button(fenetre_info, text="Valider", command=afficher_missions_jour)
    bouton_valider.pack(pady=5) 

def generer_trajet_google_maps(missions):
    url_base = "https://www.google.com/maps/dir/"

    # Ajouter "Ma position" comme première étape
    coordonnees = []

    for mission in missions:
        loc = Localisation(mission.id_localisation_a)
        coordonnees.append(f"{loc.longitude},{loc.latitude}")

    url = url_base + "/".join(coordonnees)
    webbrowser.open_new_tab(url)


# Création de la fenêtre principale
root = tk.Tk()
root.title("Application de livraison")
global username
livreur = Livreur(int(global_var.username))  # ID du livreur à récupérer
camion = Camion(livreur.id_camion)
# Création et placement des éléments dans la fenêtre
welcome_label = tk.Label(root, text=f"Bienvenue {livreur.prenom} !", font=("Arial", 24))
welcome_label.pack(pady=20)

# Bouton pour afficher les informations du livreur et les 10 dernières missions
button_afficher_infos = tk.Button(root, text="Afficher mes Informations", command=lambda: afficher_informations(livreur))
button_afficher_infos.pack(pady=10)

button_afficher_infos = tk.Button(root, text="Afficher les missions disponibles", command=lambda: afficher_informations(livreur))
button_afficher_infos.pack(pady=10)

button_afficher_missions = tk.Button(root, text="Afficher mes Missions", command=lambda: afficher_mes_missions(livreur))
button_afficher_missions.pack(pady=10)

button_afficher_missions = tk.Button(root, text="Afficher mes missions d'un jour", command=lambda: choisir_jour(livreur))
button_afficher_missions.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()

