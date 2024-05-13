import os
import sqlite3
import ast

# Get the directory containing this script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Connect to the database in that directory
conn = sqlite3.connect(os.path.join(dir_path, 'projet.db'))
cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM mission WHERE id_livreur = 1"
)
results = cursor.fetchall()
print(results)
conn.commit()
conn.close()