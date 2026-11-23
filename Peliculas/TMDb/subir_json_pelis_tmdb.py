import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


load_dotenv()

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def importar_tmdb():

    with open("peliculas_tmdb.json", "r", encoding="utf-8") as f:
        peliculas = json.load(f)

    db = SessionLocal()

    try:
        total = len(peliculas)

        for num, p in enumerate(peliculas, start=1):

            titulo = p.get("title")
            valoracion = p.get("vote_average")
            duracion = p.get("runtime")
            fecha = p.get("release_date")
            paises = p.get("origin_country") or []
            generos_lista = p.get("genres") or []
            presupuesto = p.get("budget")
            recaudacion = p.get("revenue")

            if not titulo:
                continue

            anio = None
            if fecha:
                anio = int(fecha[:4])

            paises_texto = ", ".join(paises)

            detalles = json.dumps({
                "budget": presupuesto,
                "revenue": recaudacion
            })

            query_buscar = text("""
                SELECT id
                FROM entretenimiento_audiovisual
                WHERE titulo = :titulo
                AND tipo = 'pelicula'
                AND anio_salida IS NOT DISTINCT FROM :anio;
            """)

            resultado = db.execute(query_buscar, {
                "titulo": titulo,
                "anio": anio
            }).first()

            if resultado:
                entretenimiento_id = resultado[0]

                query_actualizar = text("""
                    UPDATE entretenimiento_audiovisual
                    SET duracion_minutos = :duracion,
                        origin_country = :paises,
                        detalles_extras = CAST(:detalles AS jsonb)
                    WHERE id = :id;
                """)

                db.execute(query_actualizar, {
                    "duracion": duracion,
                    "paises": paises_texto,
                    "detalles": detalles,
                    "id": entretenimiento_id
                })

            else:
                query_item = text("""
                    INSERT INTO entretenimiento_audiovisual
                        (titulo, tipo, anio_salida,
                         duracion_minutos, origin_country,
                         detalles_extras)
                    VALUES
                        (:titulo, 'pelicula', :anio,
                         :duracion, :paises,
                         CAST(:detalles AS jsonb))
                    RETURNING id;
                """)

                resultado_insert = db.execute(query_item, {
                    "titulo": titulo,
                    "anio": anio,
                    "duracion": duracion,
                    "paises": paises_texto,
                    "detalles": detalles
                })

                entretenimiento_id = resultado_insert.scalar()

            if valoracion is not None:

                query_val = text("""
                    INSERT INTO valoraciones
                        (entretenimiento_id, fuente, puntuacion, escala)
                    VALUES
                        (:id, 'tmdb', :valoracion, 10)
                    ON CONFLICT (entretenimiento_id, fuente)
                    DO UPDATE SET puntuacion = EXCLUDED.puntuacion;
                """)

                db.execute(query_val, {
                    "id": entretenimiento_id,
                    "valoracion": valoracion
                })

            for nombre_genero in generos_lista:

                query_genero = text("""
                    INSERT INTO generos (nombre)
                    VALUES (:nombre)
                    ON CONFLICT (nombre)
                    DO UPDATE SET nombre = EXCLUDED.nombre
                    RETURNING id;
                """)

                resultado_genero = db.execute(
                    query_genero, {"nombre": nombre_genero}
                )

                genero_id = resultado_genero.scalar()

                query_relacion = text("""
                    INSERT INTO entretenimiento_generos
                        (entretenimiento_id, genero_id)
                    VALUES (:entretenimiento_id, :genero_id)
                    ON CONFLICT DO NOTHING;
                """)

                db.execute(query_relacion, {
                    "entretenimiento_id": entretenimiento_id,
                    "genero_id": genero_id
                })

            if num % 25 == 0:
                print(f"{num}/{total} películas procesadas")

        db.commit()
        print("¡Importación completada con éxito!")
        print("Películas procesadas:", total)

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    importar_tmdb()
