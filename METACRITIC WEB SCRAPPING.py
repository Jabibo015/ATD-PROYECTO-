# -*- coding: utf-8 -*-
"""
WEB SCRAPPING SELENIUM METACRITIC (PROYECTO ATD)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

# ______________________________________________________________________________________________________________-

# Act 1: Cargar la página web

driver = webdriver.Chrome()
driver.get("https://www.metacritic.com/") # Cambiar la página web
driver.implicitly_wait(10)


# Act 2: Aceptar cookies

#1º forma, menos eficiente si hay muchos:
#boton_aceptar = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler") 

#boton_aceptar = driver.find_element(by=By.ID, value="save-button")


#2º forma, más eficiente si hay muchos porque vas recorriendo:
    
"""
<button id="onetrust-accept-btn-handler">I Accept</button>
<div id="onetrust-button-group-parent" class="ot-sdk-columns has-reject-all-button ot-sdk-two"><div id="onetrust-button-group"><button id="onetrust-accept-btn-handler">I Accept</button> <button id="onetrust-reject-all-handler">Reject All</button> <button id="onetrust-pc-btn-handler" aria-label="Show Purposes, Opens the preference center dialog">Show Purposes</button></div></div>
"""

boton_aceptar = driver.find_element(by=By.ID, value="onetrust-accept-btn-handler")
print(boton_aceptar.text)
boton_aceptar.click()


#Act 3: Meterte en un subapartado (Movies)

"""
<button class="c-site-header-mobile-menu" data-testid="mobile-menu-button"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1.29em" height="1em" viewBox="0 0 18 14" class="iconify iconify--core w-4.5 h-3.75 text-white"><g fill="none"><path d="M1 1h16M1 7h16M1 13h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"></path></g></svg></button>
"""

#Meterte al apartado del menú 

boton_menu = driver.find_element(by=By.CLASS_NAME, value="c-site-header-mobile-menu")
boton_menu.click()


"""
<button class="c-site-header-mobile-menu-flyout__submenu-button">Explore Movies <span class="iconify i-core:chevron-right ml-2 size-5" aria-hidden="true"></span></button>
"""

#Meterte a subapartado Explore movies

boton_explorar_movies = driver.find_elements(by=By.CLASS_NAME, value="c-site-header-mobile-menu-flyout__submenu-button")

# Como existen varios botones con el mismo value, buscar específicamente el de 'Explore Movies'

for boton in boton_explorar_movies:
   if boton.text == "Explore Movies":
      boton.click()
   else:
      pass

#Meterse al subapartado de 'Best Movies of All Time'

boton_best_movies = driver.find_element(by=By.LINK_TEXT, value="Best Movies of All Time")
boton_best_movies.click()
time.sleep(2)

# Lista con todas las películas de la página 

"""
Copiamos y pegamos la clase

<h3 data-testid="product-title" class="m-0 text-base leading-5.5 font-bold lg:overflow-hidden lg:text-ellipsis lg:line-clamp-1 lg:max-h-5.5 lg:wrap-break-word"><span>27. </span><span>Au hasard Balthazar</span></h3>
"""

# Metemos las peliculas en una lista

lista_peliculas = driver.find_elements(by=By.CLASS_NAME, value="m-0")

for elemento in lista_peliculas:
    print(elemento.text)


# Para ver la lista completa de pelis

print(f"Total: {len(lista_peliculas)}")

for i, elemento in enumerate(lista_peliculas, start=1):
    spans = elemento.find_elements(By.TAG_NAME, "span")
    print(i, spans[1].text)



# ______________________________________________________________________________________________________________

# A tener en cuenta:
    
    # 1. Cuando hay una condición for utilizar find_elements
    # 2. Cuando se hace directamente boton.click() sin condición, utilizar find_element
    # 3. Si no se puede encontrar el elemento por botón, hacerlo por texto
    
# ______________________________________________________________________________________________________________

# Buscamos toda la información de cada película



# ______________________________________________________________________________________________________________

# Metemos la información en una lista

from datetime import datetime

# Lista vacía donde meteremos todas las películas 

peliculas = []

# Función para añadir toda la información dentro de la lista

def agregar_pelicula(titulo, valoracion, plataforma, generos, director, año_salida, duracion):
    peliculas.append({
        "titulo": titulo,
        "valoracion": valoracion,
        "plataforma": plataforma,
        "generos": generos,
        "director": director,
        "año_salida": año_salida,
        "duracion": duracion,
        "fecha_extraccion": datetime.now(),
    })


"""
# Para pasarlo a JSON
import json

datos = {
    "peliculas": peliculas
}

json_resultado = json.dumps(datos, ensure_ascii=False, indent=4)
print(json_resultado)

"""

