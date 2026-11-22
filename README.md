# ATD-PROYECTO-
Este repositorio contiene los scripts desarrollados para extraer, limpiar y cargar datos de películas, series y videojuegos desde distintas plataformas (IMDb, Letterboxd, Metacritic y Backloggd) hacia una base de datos relacional en Supabase (PostgreSQL).

El sistema unifica la información de las distintas fuentes, normaliza sus escalas de puntuación y gestiona las relaciones de directores, actores y títulos originales evitando duplicados.

---

## Estructura del Repositorio

El repositorio está organizado en tres carpetas principales según el tipo de contenido audiovisual, conteniendo cada una de ellas las subcarpetas correspondientes a cada plataforma:

```text
📦 ATD-PROYECTO-
 ┣ 📂 peliculas/
 ┃  ┣ 📂 letterboxd/
 ┃  ┣ 📂 imdb/
 ┃  ┣ 📂 metacritic/
 ┃  ┗ 📂 tmbd/
 ┃
 ┣ 📂 series/
 ┃  ┣ 📂 imdb/
 ┃  ┗ 📂 tmdb/
 ┗ 📂 videojuegos/
    ┣ 📂 backloggd/
    ┣ 📂 metacritic/
    ┣ 📂 igdb/
    ┗ 📂 imdb/


```

* **`peliculas/`**: Contiene los scripts de scraping y procesamiento para películas (Letterboxd, IMDb, Metacritic).
* **`series/`**: Contiene los scripts de extracción y gestión para series de televisión (IMDb, TMDB).
* **`videojuegos/`**: Contiene los scripts orientados a la obtención de datos de videojuegos (Backloggd, Metacritic, IGDB).

---

## Configuración y Uso

### Requisitos

Instalar las librerías necesarias para ejecutar los scripts de automatización y conexión a bases de datos:

```bash
pip install sqlalchemy psycopg2-binary python-dotenv selenium undetected-chromedriver

```

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con los datos de conexión de Supabase:

```env
DB_HOST=tu_host
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu_contraseña

```

### Ejecución

1. Navegar a la carpeta correspondiente (`peliculas/`, `series/` o `videojuegos/`) y entrar en la plataforma deseada.
2. Ejecutar el script de scraping correspondiente para generar el archivo de datos (por ejemplo, `imdb_series_original.py`).
3. Ejecutar el script de importación para volcar los registros procesados en la base de datos de Supabase.

```

