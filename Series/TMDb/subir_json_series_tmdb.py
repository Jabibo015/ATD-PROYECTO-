
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


def importar_series():

    with open("series_tmdb.json", "r", encoding="utf-8") as f:
        series = json.load(f)

    db = SessionLocal()

    try:
        total = len(series)

        for num, s in enumerate(series, start=1):

            titulo = s.get("name")
            valoracion = s.get("vote_average")
            duracion = s.get("episode_run_time")
            fecha = s.get("first_air_date")
            paises = s.get("origin_country") or []
            generos_lista = s.get("genres") or []
            temporadas = s.get("number_of_seasons")
            episodios = s.get("number_of_episodes")
            creadores = s.get("creadores") or []
            directores = s.get("directores") or []
            actores = s.get("actores") or []

            if not titulo:
                continue

            anio = None
            if fecha:
                anio = int(fecha[:4])

            if duracion is not None:
                duracion = round(duracion)

            paises_texto = ", ".join(paises)

            detalles = json.dumps({
                "number_of_seasons": temporadas,
                "number_of_episodes": episodios,
                "first_air_date": fecha,
                "creadores": creadores,
                "directores": directores,
                "actores": actores
            }, ensure_ascii=False)

            query_buscar = text("""
                SELECT id
                FROM entretenimiento_audiovisual
                WHERE titulo = :titulo
                AND tipo = 'serie'
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
                        (:titulo, 'serie', :anio,
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
                    DO UPDATE SET
                        puntuacion = EXCLUDED.puntuacion,
                        escala = EXCLUDED.escala;
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
                print(f"{num}/{total} series procesadas")

        db.commit()
        print("¡Importación completada con éxito!")
        print("Series procesadas:", total)

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    importar_series()
