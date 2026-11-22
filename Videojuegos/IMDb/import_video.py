# Subida de json videojuegos imdb a Supabase
"""

@author: aymrl
"""


#NO VOLVER A EJECUTAR, YA SE EJECUTÓ.
from http.client import CONFLICT
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


def importar_imdb():
    # 1. Cargar el archivo JSON
    with open("videojuegos_imdb.json", "r", encoding="utf-8") as f:
        videojuegos = json.load(f)

    db = SessionLocal() # Crear una sesión para interactuar con la base de datos , por comodidad lo guardamos en la variable db

    try:
        total = len(videojuegos)

        for num, p in enumerate(videojuegos, start=1):
            titulo = p.get("titulo")
            valoracion = p.get("valoracion")
            fecha_extraccion = p.get("fecha_extraccion")
            fecha_salida = p.get("fecha_salida")
            # Si el videojuego no tiene título, lo saltamos
            if not titulo:
                continue

            # 2. Buscar el videojuego para evitar duplicados
            query_buscar = text("""
                SELECT id
                FROM entretenimiento_audiovisual
                WHERE titulo = :titulo AND tipo = 'videojuego';
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
                    VALUES (:titulo, 'videojuego')
                    RETURNING id;
                """)

                resultado_insert = db.execute(
                    query_item, {"titulo": titulo}
                )
                entretenimiento_id = resultado_insert.scalar()

            # 3. Insertar la valoración, si existe
            # ON CONFLICT (entretenimiento_id, fuente) DO NOTHING evita duplicados en caso de que ya exista una valoración para ese videojuego y fuente
            if valoracion is not None:
                query_val = text("""
                    INSERT INTO valoraciones
                        (entretenimiento_id, fuente, puntuacion, escala)
                    VALUES
                        (:entretenimiento_id, 'imdb', :puntuacion, 10)
                    ON CONFLICT (entretenimiento_id, fuente) DO NOTHING;
                """)

                db.execute(query_val, {
                    "entretenimiento_id": entretenimiento_id,
                    "puntuacion": valoracion
                })
            # 4. Actualizar la fecha/año de salida, si existe
            if fecha_salida is not None and fecha_salida != "":
                query_fecha_salida = text("""
                    UPDATE entretenimiento_audiovisual
                    SET anio_salida = :anio_salida
                    WHERE id = :entretenimiento_id AND anio_salida IS NULL;
                """)
                db.execute(query_fecha_salida, {
                    "entretenimiento_id": entretenimiento_id,
                    "anio_salida": int(fecha_salida)
                })

            # 5. Actualizar la fecha de creación/extracción, si existe
            if fecha_extraccion is not None and fecha_extraccion != "":
                query_creado = text("""
                    UPDATE entretenimiento_audiovisual
                    SET creado_en = :creado_en
                    WHERE id = :entretenimiento_id AND creado_en IS NULL;
                """)
                db.execute(query_creado, {
                    "entretenimiento_id": entretenimiento_id,
                    "creado_en": fecha_extraccion
                })

            
            # Mostrar el progreso cada 25 videojuegos , esto lo hago porque si no se hace asi tarda mucho en mostrar el progreso y parece que se ha quedado colgado
            if num % 25 == 0:
                print(f"{num}/{total} videojuegos procesadas")

        # 6. Guardar todos los cambios
        db.commit()
        print("¡Importación completada con éxito !")

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    importar_imdb()