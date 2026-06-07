import requests

def buscar_personagem(id):
    r = requests.get(
        f"https://rickandmortyapi.com/api/character/{id}",
    )

    api_name = r.json().get('name')
    return api_name
