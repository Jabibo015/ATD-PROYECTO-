import json
import time
import unicodedata

import undetected_chromedriver as uc  # pip install undetected-chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ARCHIVO_JSON = "letterbox_peliculas500mejores.json"
PAUSA = 2  # segundos de espera entre peticiones

## FUNCIÓN GENERADO CON IA PARA LIMPIAR TEXTO Y NORMALIZAR CARACTERES UNICODE , TENÍA PROBLEMAS CON ESPACIOS RAROS (\xa0) 
def limpiar_texto(texto):
  """Limpia espacios raros (\xa0) y normaliza caracteres Unicode."""
  if not texto:
    return ""
  return unicodedata.normalize("NFKC", texto).strip()
## FIN FUNCIÓN GENERADA POR IA 

# Inicializar el driver de undetected_chromedriver
driver = uc.Chrome()

try:
  # 1. Recopilar las URLs de las 5 páginas del catálogo Top 500 de Letterboxd
  urls_peliculas = []

  print("Recopilando enlaces del catálogo Top 500 de Letterboxd...")
  for pagina in range(1, 6):
    if pagina == 1:
      url_lista = "https://letterboxd.com/official/list/letterboxds-top-500-films/"
    else:
      url_lista = f"https://letterboxd.com/official/list/letterboxds-top-500-films/page/{pagina}/"

    driver.get(url_lista)
    time.sleep(2)

    # Aceptar banner de cookies en la primera carga si aparece
    if pagina == 1:
      try:
        boton_aceptar = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fc-cta-consent")
            )
        )
        boton_aceptar.click()
        time.sleep(2)
      except Exception:
        print("No apareció el banner de cookies o ya fue aceptado.")

    # Esperar a que cargue la lista de pósters
    try:
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "ul.poster-list"))
      )
    except Exception:
      print(f"No se pudo cargar la página {pagina}")
      continue

    # Extraer enlaces usando exclusivamente selectores CSS
    elementos_poster = driver.find_elements(
        By.CSS_SELECTOR, "ul.poster-list li.poster-item div.film-poster"
    )
    for el in elementos_poster:
      film_slug = el.get_attribute("data-film-slug")
      if film_slug:
        url_pelicula = f"https://letterboxd.com/film/{film_slug}/"
        if url_pelicula not in urls_peliculas:
          urls_peliculas.append(url_pelicula)

    # Respaldo si no encuentra data-film-slug directamente
    if not elementos_poster:
      enlaces = driver.find_elements(
          By.CSS_SELECTOR, "ul.poster-list a[href^='/film/']"
      )
      for en in enlaces:
        href = en.get_attribute("href")
        if href and href not in urls_peliculas:
          partes = href.strip("/").split("/")
          if "film" in partes:
            idx = partes.index("film")
            if len(partes) > idx + 1:
              slug_limpio = partes[idx + 1]
              url_limpia = f"https://letterboxd.com/film/{slug_limpio}/"
              if url_limpia not in urls_peliculas:
                urls_peliculas.append(url_limpia)


                ###BLOQUE IA #####

  print(f"Se han encontrado {len(urls_peliculas)} películas en el Top 500.")

  # Cargar JSON existente (si lo hay) para permitir reanudar la ejecución
  try:
    with open(ARCHIVO_JSON, encoding="utf-8") as f:
      peliculas = json.load(f)
  except Exception:
    peliculas = []

  pendientes = urls_peliculas[len(peliculas) :]
  print(
      f"{len(pendientes)} películas pendientes de scrapeo ({len(peliculas)} ya"
      " guardadas)."
  )

  # 2. Recorrer las fichas de las películas pendientes
  for i, url_pelicula in enumerate(pendientes, start=1):
    registro = {"titulo": None, "valoracion": None, "director": [], "actores": []}

    try:
      driver.get(url_pelicula)
      WebDriverWait(driver, 15).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "#film-page-wrapper"))
      )

      # Título de la película
      h1 = driver.find_elements(By.CSS_SELECTOR, "h1.headline-1")
      if h1:
        registro["titulo"] = limpiar_texto(h1[0].get_attribute("textContent"))

      # Valoración media
      for a in driver.find_elements(
          By.CSS_SELECTOR, "a.average-rating, a[href$='/ratings/']"
      ):
        valor = limpiar_texto(a.get_attribute("textContent"))
        if valor.replace(".", "", 1).isdigit():
          registro["valoracion"] = float(valor)
          break

      # Director(es)
      for a in driver.find_elements(By.CSS_SELECTOR, "a[href^='/director/']"):
        nombre = limpiar_texto(a.get_attribute("textContent"))
        if nombre and nombre not in registro["director"]:
          registro["director"].append(nombre)

      # Actor(es)
      for a in driver.find_elements(By.CSS_SELECTOR, "a[href^='/actor/']"):
        nombre = limpiar_texto(a.get_attribute("textContent"))
        if nombre and nombre not in registro["actores"]:
          registro["actores"].append(nombre)

      print(
          f"[{i}/{len(pendientes)}] {registro['titulo']} -> Val:"
          f" {registro['valoracion']} | Dir: {registro['director']}"
      )

    except Exception as e:
      print(f"[{i}/{len(pendientes)}] ERROR en {url_pelicula}: {e}")

    # Guardado incremental en JSON manteniendo el formato estructurado y limpio
    peliculas.append(registro)
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
      json.dump(peliculas, f, ensure_ascii=False, indent=2)

    time.sleep(PAUSA)

  # 3. Obtener y mostrar la lista con todos los títulos recopilados
  todos_los_titulos = [p["titulo"] for p in peliculas if p.get("titulo")]
  print("\n" + "=" * 50)
  print(f"LISTA DE TODOS LOS TÍTULOS ({len(todos_los_titulos)} películas):")
  print("=" * 50)
  print(todos_los_titulos)

finally:
  try:
    driver.quit()
  except OSError:
    pass