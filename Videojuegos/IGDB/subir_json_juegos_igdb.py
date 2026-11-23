
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


def importar_videojuegos():

    with open("videojuegos_igdb.json", "r", encoding="utf-8") as f:
        videojuegos = json.load(f)

    ids_fijos = {1: 2267, 20: 2286, 32: 3049, 55: 2322, 84: 3047, 121: 3046, 160: 2441, 329: 3050, 356: 2722, 375: 3045}

    db = SessionLocal()

    try:
        total = len(videojuegos)
        actualizados = 0
        valoraciones = 0
        problemas = []
        ids_utilizados = set()

        if total != 500:
            raise ValueError(f"El JSON contiene {total} videojuegos, no 500")

        for num, v in enumerate(videojuegos, start=1):

            nombre = v.get("nombre")
            user_score = v.get("user_score")
            category = v.get("category")
            themes = v.get("themes") or []
            game_modes = v.get("game_modes") or []
            player_perspective = v.get("player_perspective") or []

            if not nombre:
                problemas.append((num, nombre, "Sin nombre"))
                continue

            if num in ids_fijos:

                query_buscar = text("""
                    SELECT id, titulo
                    FROM entretenimiento_audiovisual
                    WHERE id = :id
                      AND tipo = 'videojuego';
                """)

                resultado = db.execute(query_buscar, {
                    "id": ids_fijos[num]
                }).first()

                if not resultado or resultado[1].strip().lower() != nombre.strip().lower():
                    problemas.append((num, nombre, "ID fijo incorrecto"))
                    continue

                entretenimiento_id = resultado[0]

            else:

                query_buscar = text("""
                    SELECT id
                    FROM entretenimiento_audiovisual
                    WHERE tipo = 'videojuego'
                      AND LOWER(TRIM(titulo)) = LOWER(TRIM(:nombre));
                """)

                resultados = db.execute(query_buscar, {
                    "nombre": nombre
                }).all()

                if len(resultados) != 1:
                    problemas.append((
                        num,
                        nombre,
                        f"Coincidencias en Supabase: {len(resultados)}"
                    ))
                    continue

                entretenimiento_id = resultados[0][0]

            if entretenimiento_id in ids_utilizados:
                problemas.append((num, nombre, "Registro ya utilizado"))
                continue

            ids_utilizados.add(entretenimiento_id)

            detalles = json.dumps({
                "category": category,
                "themes": themes,
                "game_modes": game_modes,
                "player_perspective": player_perspective
            }, ensure_ascii=False)

            query_actualizar = text("""
                UPDATE entretenimiento_audiovisual
                SET detalles_extras =
                    COALESCE(detalles_extras, '{}'::jsonb)
                    || CAST(:detalles AS jsonb)
                WHERE id = :id;
            """)

            db.execute(query_actualizar, {
                "detalles": detalles,
                "id": entretenimiento_id
            })

            actualizados += 1

            if user_score is not None:

                query_val = text("""
                    INSERT INTO valoraciones
                        (entretenimiento_id, fuente, puntuacion, escala)
                    VALUES
                        (:id, 'igdb', :puntuacion, 100)
                    ON CONFLICT (entretenimiento_id, fuente)
                    DO UPDATE SET
                        puntuacion = EXCLUDED.puntuacion,
                        escala = EXCLUDED.escala;
                """)

                db.execute(query_val, {
                    "id": entretenimiento_id,
                    "puntuacion": user_score
                })

                valoraciones += 1

            if num % 25 == 0:
                print(f"{num}/{total} videojuegos procesados")

        print("Videojuegos encontrados:", actualizados)
        print("Valoraciones IGDB:", valoraciones)
        print("Problemas encontrados:", len(problemas))

        for problema in problemas:
            print(problema)

        if problemas or actualizados != total:
            db.rollback()
            print("Importación cancelada para evitar emparejamientos incorrectos.")
        else:
            db.commit()
            print("¡Importación completada con éxito!")

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    importar_videojuegos()
