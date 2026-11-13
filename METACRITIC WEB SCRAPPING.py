# -*- coding: utf-8 -*-
"""
WEB SCRAPPING SELENIUM METACRITIC (PROYECTO ATD)
Sacar la lista con cada videojuego --> MEJORES 500 VIDEOJUEGOS DE METACRITIC (USER SCORE HIGH-LOW)
"""

import time
import os
import glob
import re
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

# ______________________________________________________________________________________________________________

# CONFIGURACIÓN DE CHROME

options = uc.ChromeOptions()
options.binary_location = chrome_path

options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")

prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

# ______________________________________________________________________________________________________________

# Act 1: Cargar la página web

driver = uc.Chrome(options=options, browser_executable_path=chrome_path)

# Forzar tamaño de ventana
driver.set_window_rect(
    x=50,
    y=50,
    width=950,
    height=750)

driver.execute_cdp_cmd("Network.enable", {})

driver.execute_cdp_cmd("Network.setBlockedURLs", {
    "urls": [
        "*doubleclick.net/*",
        "*googlesyndication.com/*",
        "*googleadservices.com/*",
        "*adservice.google.com/*",
        "*amazon-adsystem.com/*",
        "*adnxs.com/*"
    ]})

driver.get("https://www.metacritic.com/browse/game/?pageSize=100")
driver.implicitly_wait(10)

# ______________________________________________________________________________________________________________

# Act 2: Aceptar cookies

"""
<button id="onetrust-accept-btn-handler">I Accept</button>
"""

boton_aceptar = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
print(boton_aceptar.text)
boton_aceptar.click()

    
# ______________________________________________________________________________________________________________

# Lista donde guardaremos los 500 videojuegos

videojuegos = []

# Primero recopilamos los títulos y enlaces de las cinco páginas

juegos_enlaces = []

for pagina in range(1, 6):

    url = f"https://www.metacritic.com/browse/game/?page={pagina}&pageSize=100"
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "h3")))

    time.sleep(2)

    elementos = driver.find_elements(By.TAG_NAME, "h3")

    for elemento in elementos:
        titulo = elemento.text.strip()

        try:
            enlace = elemento.find_element(By.XPATH, "./ancestor::a[1]").get_attribute("href")

            if titulo and enlace:
                juegos_enlaces.append((titulo, enlace))

        except Exception:
            continue

    print(f"Página {pagina}: {len(juegos_enlaces)} enlaces acumulados")


print("Total de enlaces recopilados:", len(juegos_enlaces))


# Ahora entramos en cada ficha para extraer el año

for i, (titulo, enlace) in enumerate(juegos_enlaces):

    try:
        driver.get(enlace)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))

        texto_pagina = driver.find_element(By.TAG_NAME, "body").text

        # Buscar la fecha que aparece después de Released On

        resultado = re.search(
            r"Released On:\s*.*?(\d{4})",
            texto_pagina,
            re.IGNORECASE)

        if resultado:
            anio = resultado.group(1)
        else:
            anio = ""

        # Eliminar numeración inicial y año del título si lo contiene

        nombre = re.sub(r"^\s*\d+\.\s*", "", titulo)
        nombre = re.sub(r"\s*\(\d{4}\)\s*$", "", nombre)

        videojuegos.append((nombre, anio))

        print(f"{i + 1}/{len(juegos_enlaces)}: {nombre} - {anio}")

        time.sleep(1)

    except Exception as e:
        print(f"Error con {titulo}: {e}")
        videojuegos.append((titulo, ""))


# Exportar la lista a un archivo Python

with open("videojuegos.py", "w", encoding="utf-8") as archivo:

    archivo.write("videojuegos = [\n")

    for nombre, anio in videojuegos:
        archivo.write(f"    ({nombre!r}, {anio!r}),\n")

    archivo.write("]\n")


# Comprobación final

print("Total de enlaces:", len(juegos_enlaces))
print("Total de videojuegos:", len(videojuegos))
print("Archivo videojuegos.py creado correctamente.")
