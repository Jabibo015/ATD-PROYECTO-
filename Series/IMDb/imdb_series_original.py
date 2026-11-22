# Web Scraping para series de IMDB (con año de salida QUE HAY Q REVISAR PQ NO FUNCIONA)
"""
@author: aymrl
"""

import json
import re
import time
import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ARCHIVO_JSON = "imdb_series_ORIGINAL.json"

# ----Configuración optimizada para evitar que los anuncios colapsen el driver---- INICIO BLOQUE IA 
options = uc.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")

prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.notifications": 2
}
options.add_experimental_option("prefs", prefs)

#-----------FIN BLOQUE IA  ------

driver = uc.Chrome(options=options, version_main=157)

try:
    url_series = "https://www.imdb.com/es/search/title/?title_type=tv_series&num_votes=10000,&sort=user_rating,desc"
    driver.get(url_series)
    time.sleep(4)

    # Aceptar cookies 
    try:
        selector_cookies = ".icb-btn.sc-bdnyFh.sc-dlniIP.sc-iCoHzw.kTxEXP.jqScCk.kQxsXA"
        boton_aceptar = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector_cookies))
        )
        boton_aceptar.click()
        time.sleep(2)
    except Exception:
        pass

    # Bucle  "Cargar más"  
    prev_count = 0
    intentos_fallidos = 0
    
    while True:
        try:
            # botón de ver más
            boton_cargar = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.ipc-see-more__text"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_cargar)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", boton_cargar)
            
            time.sleep(3) 
            
            current_blocks = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
            current_count = len(current_blocks)
            
            if current_count >= 500:
                break
                
            if current_count == prev_count:
                intentos_fallidos += 1
                if intentos_fallidos >= 4:
                    break
            else:
                intentos_fallidos = 0 
                
            prev_count = current_count
            
        except Exception:
            break

    selector_bloque = "li.ipc-metadata-list-summary-item"
    bloques = driver.find_elements(By.CSS_SELECTOR, selector_bloque)
        
    print(f"Se van a recopilar los datos de un total de {len(bloques)} series.")
        
    # Fase 1 
    items_brutos = []

    for i, bloque in enumerate(bloques, start=1):
        try:
            titulo_elem = bloque.find_element(By.CSS_SELECTOR, "h4.ipc-title__text")
            raw_title = titulo_elem.text.strip()
            clean_title = re.sub(r'^\d+[\.\-\s]+', '', raw_title)

            # Obtener enlace a la página de dentro de cada serie (detalle)
            link_elem = bloque.find_element(By.CSS_SELECTOR, "a.ipc-title-link-wrapper")
            url_detalle = link_elem.get_attribute("href")

            # Extraer año de salida
            ano_salida = None
            try:
                anyo_elems = bloque.find_elements(By.CSS_SELECTOR, "li.ipc-inline-list__item")
                for elem in anyo_elems:
                    raw_anyo = elem.text.strip()
                    match_ano = re.search(r'\b(19\d{2}|20\d{2})\b', raw_anyo)
                    if match_ano:
                        ano_salida = int(match_ano.group(1))
                        break
            except Exception:
                pass
            # Extraer valoración
            valoracion = None
            try:
                val_elem = bloque.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
                valoracion_str = val_elem.text.strip().replace(",", ".")
                if valoracion_str:
                    valoracion = float(valoracion_str)
            except Exception:
                pass 

            items_brutos.append({
                "titulo_lista": clean_title,
                "ano_salida": ano_salida,
                "url": url_detalle,
                "valoracion": valoracion,
                "director": [],
                "actores": []
            })
        except Exception as e:
            print(f"[{i}/{len(bloques)}] ERROR en bloque de lista: {e}")

    # Fase 2: página detalle para extraer el título original
    lista_series = []
    total_items = len(items_brutos)

    for i, item in enumerate(items_brutos, start=1):
        titulo_final = item["titulo_lista"] 

        try:
            driver.get(item["url"])
            time.sleep(2) 

            elementos_original = driver.find_elements(By.XPATH, "//*[contains(text(), 'Título original:')]")
                
            if elementos_original:
                texto_completo = elementos_original[0].text
                titulo_original_limpio = texto_completo.replace("Título original:", "").strip()
                if titulo_original_limpio:
                    titulo_final = titulo_original_limpio
        except Exception as e:
            print(f"Aviso: No se pudo entrar al detalle de la serie {i}, usando título de lista: {e}")

        registro = {
            "titulo": titulo_final,
            "ano_salida": item["ano_salida"],
            "valoracion": item["valoracion"],
            "director": item["director"],
            "actores": item["actores"]
        }
            
        lista_series.append(registro)
        print(f"[{i}/{total_items}] {registro['titulo']} ({registro['ano_salida']}) -> {registro['valoracion']}")

    # Guardar el resultado en el JSON de series
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(lista_series, f, ensure_ascii=False, indent=2)

finally:
    try:
        driver.quit()
    except OSError:
        pass