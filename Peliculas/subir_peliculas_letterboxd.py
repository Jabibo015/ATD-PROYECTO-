import json
import os
import traceback # Esto sirve para imprimir la traza completa del error en caso de que ocurra una excepción.
from dotenv import load_dotenv
from sqlalchemy import create_engine, text  
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()


def crear_sesion_bd():
    """Crea la conexión a Supabase y devuelve una sesión."""
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME"),
    )
    engine = create_engine( # Crea un motor de base de datos que maneja la conexión a la base de datos.
        db_url,
        pool_pre_ping=True, # Esto permite que SQLAlchemy verifique si la conexión está viva antes de usarla, evitando errores de conexión inactiva.
        connect_args={"sslmode": "require"}, # connect args para habilitar SSL ()
    )
    SessionLocal = sessionmaker(bind=engine) # Crea una clase de sesión que se puede usar para interactuar con la base de datos .
    return SessionLocal()


def obtener_o_crear_pelicula(db, titulo):
    """Busca la película en entretenimiento_audiovisual; si no existe, la crea y devuelve su id."""
    fila = db.execute(
        text("""
            SELECT id
            FROM entretenimiento_audiovisual
            WHERE titulo = :titulo AND tipo = 'pelicula'
        """),
        {"titulo": titulo},
    ).first()

    if fila is not None:
        return fila[0]

    nuevo_id = db.execute(
        text("""
            INSERT INTO entretenimiento_audiovisual (titulo, tipo)
            VALUES (:titulo, 'pelicula')
            RETURNING id
        """),
        {"titulo": titulo},
    ).scalar() # scalar() devuelve el primer elemento de la primera fila del resultado, que en este caso es el id recién insertado.

    return nuevo_id


def guardar_valoracion_letterboxd(db, entretenimiento_id, valoracion):
    """Guarda o actualiza la valoración de Letterboxd si tiene un número válido."""
    if valoracion is None or valoracion == "" or valoracion == "N/A":
        return

    try:
        puntuacion = float(valoracion)
    except (ValueError, TypeError):
        return

    db.execute(
        text("""
            INSERT INTO valoraciones (entretenimiento_id, fuente, puntuacion, escala)
            VALUES (:entretenimiento_id, 'letterboxd', :puntuacion, 5)
            ON CONFLICT (entretenimiento_id, fuente)
            DO UPDATE SET
                puntuacion = EXCLUDED.puntuacion,
                escala = EXCLUDED.escala
        """),
        {
            "entretenimiento_id": entretenimiento_id,
            "puntuacion": puntuacion,
        },
    )


def obtener_o_crear_persona(db, tabla_persona, nombre):
    """Inserta o recupera el id de un director o actor en su tabla correspondiente."""
    persona_id = db.execute(
        text(f"""
            INSERT INTO {tabla_persona} (nombre)
            VALUES (:nombre)
            ON CONFLICT (nombre)
            DO UPDATE SET nombre = EXCLUDED.nombre
            RETURNING id
        """),
        {"nombre": nombre},
    ).scalar()

    return persona_id


def vincular_directores(db, entretenimiento_id, directores):
    """Relaciona la película con cada director en entretenimiento_directores."""
    for nombre_director in directores:
        if not nombre_director:
            continue

        director_id = obtener_o_crear_persona(db, "directores", nombre_director)

        db.execute(
            text("""
                INSERT INTO entretenimiento_directores (entretenimiento_id, director_id)
                VALUES (:entretenimiento_id, :director_id)
                ON CONFLICT DO NOTHING
            """),
            {
                "entretenimiento_id": entretenimiento_id,
                "director_id": director_id,
            },
        )


def vincular_actores(db, entretenimiento_id, actores):
    """Relaciona la película con cada actor en entretenimiento_actores."""
    for nombre_actor in actores:
        if not nombre_actor:
            continue

        actor_id = obtener_o_crear_persona(db, "actores", nombre_actor)

        db.execute(
            text("""
                INSERT INTO entretenimiento_actores (entretenimiento_id, actor_id)
                VALUES (:entretenimiento_id, :actor_id)
                ON CONFLICT DO NOTHING
            """),
            {
                "entretenimiento_id": entretenimiento_id,
                "actor_id": actor_id,
            },
        )


def importar_letterboxd():
    """Lee el JSON de películas y sube los datos a Supabase."""
    ruta_json = "letterbox_peliculas500mejores.json"
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        peliculas = json.load(archivo)

    db = crear_sesion_bd()
    total = len(peliculas)

    try:
        for posicion, pelicula in enumerate(peliculas, start=1):
            titulo = pelicula.get("titulo")
            if not titulo:
                continue

            valoracion = pelicula.get("valoracion")
            directores = pelicula.get("director") or []
            actores = pelicula.get("actores") or []

            entretenimiento_id = obtener_o_crear_pelicula(db, titulo)
            guardar_valoracion_letterboxd(db, entretenimiento_id, valoracion)
            vincular_directores(db, entretenimiento_id, directores)
            vincular_actores(db, entretenimiento_id, actores)

            if posicion % 25 == 0:
                db.commit()
                print(f"Guardadas {posicion} de {total} películas...")

        db.commit()
        print("Importación terminada correctamente.")

    except Exception as error:
        db.rollback()
        print(f"Ha ocurrido un error en la película '{pelicula.get('titulo')}': {error}")
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    importar_letterboxd()