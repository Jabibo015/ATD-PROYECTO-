# TOP 250 MOVIES

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import undetected_chromedriver as uc #   pip install undetected-chromedriver
 
url1 = "https://www.imdb.com/es/"

driver = uc.Chrome(version_main=155)
driver.get("https://www.imdb.com/es/")

time.sleep(5)

#Cookies
selector = ".icb-btn.sc-bdnyFh.sc-dlniIP.sc-iCoHzw.kTxEXP.jqScCk.kQxsXA"
boton_aceptar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
)
boton_aceptar.click()
time.sleep(5)

#Top 250 Pelis ____________________________

# Busca el botón de menú por su ID exacto
boton_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "imdbHeader-navDrawerOpen"))
)
boton_menu.click()

time.sleep(2)

#----Proporciones
screen_width = driver.execute_script("return window.screen.width;")
screen_height = driver.execute_script("return window.screen.height;")
mitad_ancho = screen_width // 2
driver.set_window_rect(x=0, y=0, width=mitad_ancho, height=screen_height)



#Boton desplegar más en peliculas
boton_desp = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[for="nav-link-categories-mov"]'))
)
boton_desp.click()
time.sleep(2)

#Top 250 button
boton_top250 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Ir a Top 250 películas"]'))
)
driver.execute_script("arguments[0].click();", boton_top250)
time.sleep(1)


#Top 250 list
pelis_list=driver.find_elements(by=By.CLASS_NAME, value="ipc-metadata-list-summary-item__c")

for peli in pelis_list:
    print(peli)

time.sleep(2)


#titulo_list & valoracion list prueba
titulos_elementos = driver.find_elements(By.CLASS_NAME, value= "ipc-title__text")

for elemento in titulos_elementos:
  print(elemento.text)

valoracion_elementos = driver.find_elements(By.CLASS_NAME, value="ipc-rating-star--rating")
for elemento in valoracion_elementos:
  print(elemento.text)



