import requests

# URL de l'API
url = "http://127.0.0.1:8000/api/V1/rooms/rooms/"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM3NjQ1MDg2LCJpYXQiOjE3Mzc2MTYyODYsImp0aSI6ImIyNDQyMTVhZGQ0NzQ5ZTZhMjA4YTQxNzIwOTkzMGQ0IiwidXNlcl9pZCI6MiwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOiJzdXBlcl9hZG1pbiIsImRpcmVjdGlvbiI6IkRTSU4iLCJlbWFpbCI6InJvbnNhcmRoaWVuQGdtYWlsLmNvbSJ9.a6Y0z0migKDK3Hz4zDEKVxVwTxjvjrs6UKJwHbRkRfw"
}


data = {
    "name": "Salle Polyvalente",
    "direction": 7,
    "capacite": 100,
    "localisation": "Bâtiment A, étage 1",
    "equipements[0]": 1,
    "equipements[1]": 2,
    "equipements[2]": 3
}

# Chemins des fichiers d'image
files = [
    ('add_images[0][image]', ('Architecture.png', open('C:/Users/hienr/Downloads/Architecture.png', 'rb'), 'image/png')),
    ('add_images[0][description]', (None, "Image de la salle principale"))
    #('add_images[1][image]', ('paa.png', open('C:/Users/hienr/Downloads/paa.png', 'rb'), 'image/png')),
    #('add_images[1][description]', (None, "Image secondaire pour la salle"))
]

# Requête POST
response = requests.post(url, headers=headers, data=data, files=files)

# Afficher la réponse
print("Statut :", response.status_code)
print("Réponse :", response.json())
