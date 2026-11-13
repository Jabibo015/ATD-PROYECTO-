
import requests
from bs4 import BeautifulSoup



videojuegos = ["Disco Elysium", "Hollow Knight", "Celeste", "Stardew Valley", "Undertale", "Hades", "Minecraft", "Terraria", "Portal 2", "Outer Wilds", "Cuphead", "Dead Cells", "Slay the Spire", "The Witness", "Tunic", "Animal Well", "Chants of Sennaar", "Cocoon", "Dredge", "A Short Hike", "Night in the Woods", "Return of the Obra Dinn", "The Case of the Golden Idol", "Baba Is You", "Pizza Tower", "Balatro", "Inscryption", "Katana ZERO", "Hyper Light Drifter", "CrossCode", "OneShot", "OMORI", "Rain World", "Signalis", "GRIS", "FEZ", "Papers, Please", "The Talos Principle", "The Forgotten City", "Pentiment", "Citizen Sleeper", "Norco", "In Stars and Time", "Void Stranger", "ZeroRanger", "Astlibra Revision", "Phoenotopia: Awakening", "LISA: The Painful", "The Legend of Zelda: Breath of the Wild", "NieR: Automata"]

resultados = []

for nombre in videojuegos:

    nombre_url = nombre.lower().replace(",", "").replace(":", "").replace(" ", "-")
    url = "https://backloggd.com/games/" + nombre_url + "/"

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")
        texto = soup.get_text(" ", strip=True)
        
        if "Avg Rating" in texto:
            nota = texto.split("Avg Rating", 1)[1].split()[0]

            print(nombre, ":", nota)

            resultados.append({
                "titulo": nombre,
                "valoracion": nota
            })

        else:
            print(nombre, ": Valoración no encontrada")

    except requests.RequestException:
        print(nombre, ": No se ha podido consultar")
