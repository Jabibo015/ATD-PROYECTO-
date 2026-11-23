import json
import os
import traceback
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
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"},
    )
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def convertir_duracion(duracion_raw):
    """Convierte duracion_min a entero de minutos o devuelve None si no es válido."""
    if duracion_raw is None or duracion_raw == "" or duracion_raw == "N/A":
        return None
    try:
        return int(round(float(duracion_raw)))
    except (ValueError, TypeError):
        return None


def obtener_o_crear_videojuego(db, titulo, duracion_minutos):
    """Busca el videojuego; si no existe, lo crea, y actualiza su duración si aplica."""
    fila = db.execute(
        text("""
            SELECT id
            FROM entretenimiento_audiovisual
            WHERE titulo = :titulo AND tipo = 'videojuego'
        """),
        {"titulo": titulo},
    ).first()

    if fila is not None:
        entretenimiento_id = fila[0]
        if duracion_minutos is not None:
            db.execute(
                text("""
                    UPDATE entretenimiento_audiovisual
                    SET duracion_minutos = :duracion_minutos
                    WHERE id = :id
                """),
                {
                    "id": entretenimiento_id,
                    "duracion_minutos": duracion_minutos,
                },
            )
        return entretenimiento_id

    nuevo_id = db.execute(
        text("""
            INSERT INTO entretenimiento_audiovisual (titulo, tipo, duracion_minutos)
            VALUES (:titulo, 'videojuego', :duracion_minutos)
            RETURNING id
        """),
        {
            "titulo": titulo,
            "duracion_minutos": duracion_minutos,
        },
    ).scalar()

    return nuevo_id


def guardar_valoracion_backloggd(db, entretenimiento_id, valoracion):
    """Guarda o actualiza la valoración de Backloggd si tiene un número válido."""
    if valoracion is None or valoracion == "" or valoracion == "N/A":
        return

    try:
        puntuacion = float(valoracion)
    except (ValueError, TypeError):
        return

    db.execute(
        text("""
            INSERT INTO valoraciones (entretenimiento_id, fuente, puntuacion, escala)
            VALUES (:entretenimiento_id, 'backloggd', :puntuacion, 5)
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


def obtener_o_crear_etiqueta(db, tabla, nombre):
    """Inserta o recupera el id de un género o plataforma en su tabla."""
    etiqueta_id = db.execute(
        text(f"""
            INSERT INTO {tabla} (nombre)
            VALUES (:nombre)
            ON CONFLICT (nombre)
            DO UPDATE SET nombre = EXCLUDED.nombre
            RETURNING id
        """),
        {"nombre": nombre},
    ).scalar()

    return etiqueta_id


def vincular_generos(db, entretenimiento_id, generos):
    """Relaciona el videojuego con cada género en entretenimiento_generos."""
    for nombre_genero in generos:
        if not nombre_genero:
            continue

        genero_id = obtener_o_crear_etiqueta(db, "generos", nombre_genero)

        db.execute(
            text("""
                INSERT INTO entretenimiento_generos (entretenimiento_id, genero_id)
                VALUES (:entretenimiento_id, :genero_id)
                ON CONFLICT DO NOTHING
            """),
            {
                "entretenimiento_id": entretenimiento_id,
                "genero_id": genero_id,
            },
        )


def vincular_plataformas(db, entretenimiento_id, plataformas):
    """Relaciona el videojuego con cada plataforma en entretenimiento_plataformas."""
    for nombre_plataforma in plataformas:
        if not nombre_plataforma:
            continue

        plataforma_id = obtener_o_crear_etiqueta(db, "plataformas", nombre_plataforma)

        db.execute(
            text("""
                INSERT INTO entretenimiento_plataformas (entretenimiento_id, plataforma_id)
                VALUES (:entretenimiento_id, :plataforma_id)
                ON CONFLICT DO NOTHING
            """),
            {
                "entretenimiento_id": entretenimiento_id,
                "plataforma_id": plataforma_id,
            },
        )


def importar_backloggd():
    """Lee videojuegos.json y sube los datos a Supabase."""
    ruta_json = "backloggd_videojuegos500mejores.json"
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        videojuegos = json.load(archivo)

    db = crear_sesion_bd()
    total = len(videojuegos)
    videojuego_actual = None

    try:
        for posicion, juego in enumerate(videojuegos, start=1):
            videojuego_actual = juego
            titulo = juego.get("titulo")
            if not titulo:
                continue

            # Soporta tanto "Valoración" como "valoracion" y "Plataformas" como "plataformas"
            valoracion = juego.get("Valoración", juego.get("valoracion"))
            duracion_minutos = convertir_duracion(juego.get("duracion_min"))
            generos = juego.get("generos") or []
            plataformas = juego.get("Plataformas", juego.get("plataformas")) or []

            entretenimiento_id = obtener_o_crear_videojuego(
                db, titulo, duracion_minutos
            )
            guardar_valoracion_backloggd(db, entretenimiento_id, valoracion)
            vincular_generos(db, entretenimiento_id, generos)
            vincular_plataformas(db, entretenimiento_id, plataformas)

            if posicion % 25 == 0:
                db.commit()
                print(f"Guardados {posicion} de {total} videojuegos...")

        db.commit()
        print("Importación de videojuegos terminada correctamente.")

    except Exception as error:
        db.rollback()
        titulo_error = (
            videojuego_actual.get("titulo") if videojuego_actual else "desconocido"
        )
        print(f"Ha ocurrido un error en el videojuego '{titulo_error}': {error}")
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    importar_backloggd()