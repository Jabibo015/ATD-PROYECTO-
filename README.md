# ATD-PROYECTO-
Este repositorio contiene los scripts desarrollados para extraer, limpiar y cargar datos de películas, series y videojuegos desde distintas plataformas (IMDb, Letterboxd, Metacritic y Backloggd) hacia una base de datos relacional en Supabase (PostgreSQL).

El sistema unifica la información de las distintas fuentes, normaliza sus escalas de puntuación (escala 10 en IMDb, escala 5 en Letterboxd) y gestiona las relaciones de directores, actores y títulos originales evitando duplicados.

---

## Estructura del Repositorio

Los archivos del proyecto están organizados según su función dentro del flujo de trabajo:

### 1. Scrappers principales (Generación de JSON)
Scripts definitivos encargados de navegar por las webs, limpiar los campos (títulos originales, años, repartos) y exportar los datos en formato `.json`:
* `scrapper_letterbox.py`: Pruebas iniciales sobre IMDb.



### 2. Scripts de importación a Supabase
Scripts que leen los archivos `.json` generados y realizan la inserción en PostgreSQL mediante `SQLAlchemy` y `psycopg2`:
* `letterbox.py`: Carga los datos extraídos de Letterboxd en la base de datos.


### 3. Datasets generados
* `imdb_series.json`: Archivo con los datos limpios de las series extraídas de IMDb, listo para su importación.

### 4. Pruebas iniciales de extracción
Scripts de prueba realizados al inicio del proyecto para comprobar la viabilidad del scraping y los selectores de cada página:
* `imdb_scraping.py`: Pruebas iniciales sobre IMDb.
* `scrapper.py`: Primeras pruebas de extracción sobre Letterboxd.
* `METACRITIC WEB SCRAPPING.py`: Pruebas de scraping en Metacritic.
* `scrapping backloggd.py`: Pruebas de extracción de videojuegos en Backloggd.
* `api pelis.py`: Pruebas de obtención de datos mediante API externa.

### 5. Archivos antiguos / Descartados
* `LISTA_500_MEJORES...`: Archivo de referencia de las 500 mejores obras (solo es válida la versión del segundo commit; la primera está desactualizada).
* `Lista títulos películas`: Listado inicial descartado porque no incluía el año de estreno.

---

## Configuración y Uso

### Requisitos
Instalar las librerías necesarias:
```bash
pip install sqlalchemy psycopg2-binary python-dotenv selenium undetected-chromedriver
```

### Variables de entorno
Crear un archivo `.env` en la raíz del proyecto con los datos de conexión de Supabase:

```env
DB_HOST= host
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña
```

### Ejecución
1. Ejecutar el scraper correspondiente (---) para generar el archivo `.json`.
2. Ejecutar el script de carga (`letterbox.py`,`import-imdb_series.py`) para subir los registros a Supabase.
