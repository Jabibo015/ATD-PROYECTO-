import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMjAyNTZkYmIyM2JmMDY4NDA5YTEwZmE3NTg3OTViNyIsIm5iZiI6MTc5MTI2OTk2My42MTYsInN1YiI6IjZhYzQ5YzRiNmI2MmJkMGM2YWYyNjdjMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.2WGL5G5EIpJZvfsFn1IWBNDXXlmvwoab0gIv1iylOEo"
url = "https://api.themoviedb.org/3/movie/top_rated"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

peliculas = []
titulos = []

pagina = 1

while len(peliculas) < 500:

    parametros = {
        "page": pagina
    }

    respuesta = requests.get(url, headers=headers, params=parametros)
    respuesta.raise_for_status()

    datos = respuesta.json()

    for pelicula in datos["results"]:

        if pelicula["vote_count"] >= 3000:

            info = {
                "id": pelicula["id"],
                "titulo": pelicula["title"],
                "fecha": pelicula["release_date"],
                "valoracion": pelicula["vote_average"],
                "votos": pelicula["vote_count"]
            }

            peliculas.append(info)
            titulos.append(pelicula["title"])

            if len(peliculas) == 500:
                break

    if pagina >= datos["total_pages"]:
        break

    pagina += 1

print("Películas obtenidas:", len(peliculas))

#for pelicula in peliculas:
    #print(pelicula["titulo"], pelicula["valoracion"], pelicula["fecha"])

#print("Títulos:", titulos)

#for titulo in titulos:
    #print(titulo)

def guardar_json(peliculas):
    with open("peliculas.json", "w", encoding="utf-8") as fichero:
        json.dump(peliculas, fichero, ensure_ascii=False, indent=4)

guardar_json(peliculas)