



# NO VOLVAÍS A EJECUTAR ESTE ARCHIVO PORFAVOR , EL CONTENIDO YA ESTA EN LA BASE DE DATOS DE SUPABASE 


import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


# Cargar las variables de entorno
load_dotenv()

# Conexión con la base de datos de Supabase , los datos que se llaman estan en el .env
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(db_url, pool_pre_ping=True) #Esto sirve para conectarse a la base de datos de Supabase
SessionLocal = sessionmaker(bind=engine) # Aquí se crea una sesión para interactuar con la base de datos podremos usarla para hacer consultas, inserciones, etc.


def importar_letterboxd():
    # 1. Cargar el archivo JSON
    with open("peliculas_letterboxd.json", "r", encoding="utf-8") as f:
        peliculas = json.load(f)

    db = SessionLocal() # Crear una sesión para interactuar con la base de datos , por comodidad lo guardamos en la variable db

    try:
        total = len(peliculas)

        for num, p in enumerate(peliculas, start=1):
            titulo = p.get("titulo")
            valoracion = p.get("valoracion")
            directores_lista = p.get("director") or []
            actores_lista = p.get("actores") or []

            # Si la película no tiene título, la saltamos
            if not titulo:
                continue

            # 2. Buscar la película para evitar duplicados
            query_buscar = text("""
                SELECT id
                FROM entretenimiento_audiovisual
                WHERE titulo = :titulo AND tipo = 'pelicula';
            """)

            resultado_busqueda = db.execute(
                query_buscar, {"titulo": titulo}
            ).first() # first() devuelve la primera fila del resultado, o None si no hay resultados

            if resultado_busqueda:
                # Si ya existe, reutilizamos su ID
                entretenimiento_id = resultado_busqueda[0]
            else:
                # Si no existe, la insertamos y obtenemos su ID
                query_item = text("""
                    INSERT INTO entretenimiento_audiovisual (titulo, tipo)
                    VALUES (:titulo, 'pelicula')
                    RETURNING id;
                """)

                resultado_insert = db.execute(
                    query_item, {"titulo": titulo}
                )
                entretenimiento_id = resultado_insert.scalar()

            # 3. Insertar la valoración, si existe
            # ON CONFLICT (entretenimiento_id, fuente) DO NOTHING evita duplicados en caso de que ya exista una valoración para esa película y fuente
            if valoracion is not None:
                query_val = text("""
                    INSERT INTO valoraciones
                        (entretenimiento_id, fuente, puntuacion, escala)
                    VALUES
                        (:entretenimiento_id, 'letterboxd', :puntuacion, 5)
                    ON CONFLICT (entretenimiento_id, fuente) DO NOTHING;
                """)

                db.execute(query_val, {
                    "entretenimiento_id": entretenimiento_id,
                    "puntuacion": valoracion
                })

            # 4. Procesar y relacionar los directores
            for nombre_director in directores_lista:
                if not nombre_director:
                    continue

                # Insertar el director o recuperar su ID si ya existe
                query_dir = text("""
                    INSERT INTO directores (nombre)
                    VALUES (:nombre)
                    ON CONFLICT (nombre)
                    DO UPDATE SET nombre = EXCLUDED.nombre
                    RETURNING id;
                """)

                resultado_dir = db.execute(
                    query_dir, {"nombre": nombre_director}
                )
                director_id = resultado_dir.scalar() # scalar() devuelve el primer valor de la primera fila del resultado, en este caso el ID del director

                # Crear la relación entre la película y el director
                query_rel_dir = text("""
                    INSERT INTO entretenimiento_directores
                        (entretenimiento_id, director_id)
                    VALUES (:entretenimiento_id, :director_id)
                    ON CONFLICT DO NOTHING;
                """)

                db.execute(query_rel_dir, {
                    "entretenimiento_id": entretenimiento_id,
                    "director_id": director_id
                })

            # 5. Procesar y relacionar los actores
            for nombre_actor in actores_lista:
                if not nombre_actor:
                    continue

                # Insertar el actor o recuperar su ID si ya existe
                query_act = text("""
                    INSERT INTO actores (nombre)
                    VALUES (:nombre)
                    ON CONFLICT (nombre)
                    DO UPDATE SET nombre = EXCLUDED.nombre
                    RETURNING id;
                """)

                resultado_act = db.execute(
                    query_act, {"nombre": nombre_actor}
                )
                actor_id = resultado_act.scalar()

                # Crear la relación entre la película y el actor
                query_rel_act = text("""
                    INSERT INTO entretenimiento_actores
                        (entretenimiento_id, actor_id)
                    VALUES (:entretenimiento_id, :actor_id)
                    ON CONFLICT DO NOTHING;
                """)

                db.execute(query_rel_act, {
                    "entretenimiento_id": entretenimiento_id,
                    "actor_id": actor_id
                })

            # Mostrar el progreso cada 25 películas , esto lo hago porque si no se hace asi tarda mucho en mostrar el progreso y parece que se ha quedado colgado
            if num % 25 == 0:
                print(f"{num}/{total} películas procesadas")

        # 6. Guardar todos los cambios
        db.commit()
        print("¡Importación completada con éxito !")

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    importar_letterboxd()
