import json
import time

import undetected_chromedriver as uc  # pip install undetected-chromedriver , para quitar el captcha de Letterboxd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#Titulos de las peliculas a scrapear , de la API de TMDB
Titulos = ["The Shawshank Redemption", "The Godfather", "Project Hail Mary", "Michael", "12 Angry Men", "The Godfather Part II", "Schindler's List", "The Dark Knight", "Spirited Away", "The Green Mile", "The Lord of the Rings: The Return of the King", "Dilwale Dulhania Le Jayenge", "Your Name.", "Interstellar", "Parasite", "Pulp Fiction", "The Good, the Bad and the Ugly", "Spider-Man: Brand New Day", "Forrest Gump", "Grave of the Fireflies", "Seven Samurai", "GoodFellas", "The Lord of the Rings: The Fellowship of the Ring", "Fight Club", "Life Is Beautiful", "Cinema Paradiso", "The Lord of the Rings: The Two Towers", "City of God", "Psycho", "One Flew Over the Cuckoo's Nest", "A Silent Voice: The Movie", "Spider-Man: Into the Spider-Verse", "The Empire Strikes Back", "Howl's Moving Castle", "Se7en", "Whiplash", "Inception", "The Pianist", "Once Upon a Time in America", "Spider-Man: Across the Spider-Verse", "The Silence of the Lambs", "Rear Window", "Back to the Future", "American History X", "Princess Mononoke", "The Wild Robot", "Perfect Blue", "Dead Poets Society", "Léon: The Professional", "Modern Times", "The Great Dictator", "It's a Wonderful Life", "Sunset Boulevard", "The Intouchables", "Once Upon a Time in the West", "The Matrix", "Apocalypse Now", "The Lion King", "Paths of Glory", "Miracle in Cell No. 7", "Avengers: Endgame", "Avengers:Infinity War", "Demon Slayer -Kimetsu no Yaiba- The Movie: Mugen Train", "Saving Private Ryan", "Oldboy", "Gladiator", "Green Book", "Puss in Boots: The Last Wish", "Inglourious Basterds", "Klaus", "Five Feet Apart", "The Prestige", "The Super Mario Galaxy Movie", "The Help", "Star Wars", "Coco", "The Shining", "Shutter Island", "Hacksaw Ridge", "Django Unchained", "The Handmaiden", "Alien", "Obsession","Terminator 2: Judgment Day", "Memento", "A Clockwork Orange", "Good Will Hunting", "The Usual Suspects", "The Truman Show", "The Departed", "Top Gun: Maverick", "Scarface", "Dune: Part Two", "Casablanca", "The Seventh Seal", "Vertigo", "WALL·E", "Singin' in the Rain", "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb", "Full Metal Jacket", "Taxi Driver", "Joker", "Reservoir Dogs", "Prisoners", "Incendies", "The Hunt", "Wonder", "Lock, Stock and Two Smoking Barrels", "The Father", "Eternal Sunshine of the Spotless Mind", "La Haine", "Portrait of a Lady on Fire", "Soul", "In the Mood for Love", "The Avengers", "Metropolis", "Harry Potter and the Deathly Hallows: Part 2", "Call Me by Your Name", "Some Like It Hot", "The Thing", "The Invisible Guest", "Zack Snyder's Justice League", "My Neighbor Totoro", "Memories of Murder", "There Will Be Blood", "Flow", "Hidden Figures", "Three Billboards Outside Ebbing, Missouri", "Pride & Prejudice", "The Elephant Man", "2001: A Space Odyssey", "The Lives of Others", "Lion", "For a Few Dollars More", "The Wolf of Wall Street", "Amadeus", "The Grand Budapest Hotel", "Flipped", "Oppenheimer", "The Odyssey", "Harry Potter and the Prisoner of Azkaban", "The Sting", "Ford v Ferrari", "Hachi: A Dog's Tale", "Requiem for a Dream", "Barry Lyndon", "Lawrence of Arabia", "Casino", "American Beauty", "Guillermo del Toro's Pinocchio", "Toy Story", "Gran Torino", "Gifted", "Room", "1917", "KPop Demon Hunters", "Catch Me If You Can", "The Imitation Game", "Jurassic Park", "Castle in the Sky", "Jojo Rabbit", "Dragon Ball Super: Broly", "Kill Bill: Vol. 1", "Aliens", "Before Sunrise", "The Iron Giant", "Society of the Snow", "Citizen Kane", "North by Northwest", "Cruella", "Up", "Trainspotting", "Love, Simon", "The Deer Hunter", "The Sixth Sense", "Million Dollar Baby", "No Country for Old Men", "Spider-Man: No Way Home", "BohemianRhapsody", "Braveheart", "Heat", "Coraline", "Warriors of the Wind", "Akira", "Blade Runner", "Me Before You", "Ghost in the Shell", "How to Train Your Dragon", "Rope", "12 Years a Slave", "Raiders of the Lost Ark", "Amélie", "A Bronx Tale", "Unforgiven", "Return of the Jedi", "Guardians of the Galaxy", "Chinatown", "Inside Out", "Dallas Buyers Club", "Harry Potter and the Philosopher's Stone", "Gone with the Wind", "Mulan", "About Time", "Titanic", "V for Vendetta", "La La Land", "Raging Bull", "Dragon Ball Super: Super Hero", "Gone Girl", "Ben-Hur", "The Notebook", "Captain Fantastic", "The Pursuit of Happyness", "Kill Bill: Vol. 2", "Downfall", "Wild Tales", "How to Train Your Dragon", "Monsters, Inc.", "Nobody", "Young Frankenstein", "Indiana Jones and the Last Crusade", "Dog Day Afternoon", "A Beautiful Mind", "Isle of Dogs", "The Greatest Showman", "The Nightmare Before Christmas", "The Big Lebowski", "Ratatouille", "Fargo", "Perfect Strangers", "Little Women", "Predator: Badlands", "Knives Out", "Warrior", "Kiki's Delivery Service", "Dances with Wolves", "Pirates of the Caribbean: The Curse of the Black Pearl", "Stand by Me", "Her", "Sing 2", "Snatch", "F1", "Fantastic Mr. Fox", "Carlito's Way", "A Fistful of Dollars", "The Mitchells vs. the Machines", "Logan", "Finding Nemo", "The Theory of Everything", "The Boy in the Striped Pyjamas", "Toy Story 3", "Finch", "Die Hard", "Paprika", "Rosemary's Baby", "L.A. Confidential", "Spotlight", "The Best Offer", "Love, Rosie", "I Saw the Devil", "Before Sunset", "The Perks of Being a Wallflower", "Harry Potter and the Goblet of Fire", "Mulholland Drive", "Monty Python and the Holy Grail", "Midnight Sun", "Rocky", "The Dark Knight Rises", "Into the Wild", "Scent of a Woman", "Porco Rosso", "Raya and the Last Dragon", "The Wind Rises", "Back to the Future Part II", "Dune", "Brokeback Mountain", "Mr. Nobody", "Shrek", "Straight Outta Compton", "Luca", "Pan's Labyrinth", "Zootopia", "Ip Man", "Life of Brian", "Ponyo", "Donnie Darko", "The Hateful Eight", "Misery", "The Untouchables", "Train to Busan", "The Whale", "How to Train Your Dragon: The Hidden World", "The Exorcist", "Rain Man", "A ManCalled Otto", "Rush", "A Walk to Remember", "Platoon", "Big Fish", "Mystic River", "All Quiet on the Western Front", "Three Steps AboveHeaven", "Marriage Story", "Harry Potter and the Deathly Hallows: Part 1", "The King's Speech", "Batman Begins", "The Sound of Music", "The Incredibles", "Slumdog Millionaire", "Beauty and the Beast", "Big Hero 6", "My Fault", "Hotel Rwanda", "Magnolia", "Edward Scissorhands", "Guy Ritchie's The Covenant", "Two Is a Family", "Everything Everywhere All at Once", "The Breakfast Club", "John Wick: Chapter 4", "Spirit: Stallion of the Cimarron", "The Blues Brothers", "The Martian", "The Princess Bride", "Annie Hall", "Harry Potter and the Chamber of Secrets", "The Gorge", "Nightcrawler", "Philadelphia", "The Terminator", "Little Miss Sunshine", "Jaws", "Gran Turismo", "Arrietty", "How to Train Your Dragon 2", "Black Swan", "Harry Potter and the Half-Blood Prince", "Moonrise Kingdom", "The Batman", "Harry Potter and the Order of the Phoenix", "Apocalypto", "Remember the Titans", "Cast Away", "Zootopia 2", "Iron Man", "Primal Fear", "The Gentlemen", "The Blind Side", "Aladdin", "Planet of the Apes", "What's Eating Gilbert Grape", "Brazil", "Captain America: The Winter Soldier", "The Trial of the Chicago 7", "Kubo and the Two Strings", "Amores Perros", "Avatar: Fire and Ash", "Edge of Tomorrow", "Prey", "A Dog's Purpose", "Mad Max: Fury Road", "All the Bright Places", "Arrival", "The Longest Ride", "Groundhog Day", "Atonement", "Boogie Nights","Memoirs of a Geisha", "Onward", "Another Round", "The Little Prince", "The Graduate", "Deadpool", "Get Out", "Poor Things", "Toy Story2", "The Man from Earth", "Children of Men", "The Others", "Kingsman: The Secret Service", "Tangled", "Roma", "The Last Samurai", "Twelve Monkeys", "Avatar", "Blade Runner 2049", "Guardians of the Galaxy Vol. 2", "Breakfast at Tiffany's", "The Curious Case of Benjamin Button", "Sleepers", "Godzilla Minus One", "Blue Velvet", "Billy Elliot", "Anastasia", "10 Things I Hate About You", "Frankenstein", "Seven Pounds", "American Gangster", "Sonic the Hedgehog 3", "The Kissing Booth 2", "Corpse Bride", "Thelma & Louise", "The Fifth Element", "Elemental", "Deadpool & Wolverine", "To All the Boys I've Loved Before", "The Super Mario Bros. Movie", "The Fault in Our Stars", "CoachCarter", "Ready Player One", "Predator", "Drive", "Avatar: The Way of Water", "The Wizard of Oz", "Treasure Planet", "The Game", "The Hobbit: The Desolation of Smaug", "Thor: Ragnarok", "Casino Royale", "The Butterfly Effect", "Wrath of Man", "Hot Fuzz", "Ex Machina", "The Irishman", "Gattaca", "Moana", "The Emperor's New Groove", "Changeling", "Encanto", "Searching", "Moon", "Lilo & Stitch", "A Few GoodMen", "Blood Diamond", "Halloween", "I Origins", "Ferris Bueller's Day Off", "Girl, Interrupted", "Lost Highway", "Mary Poppins", "Manchester by the Sea", "Fury", "The Conjuring", "Shaun of the Dead", "Spies in Disguise", "Who Framed Roger Rabbit", "The Revenant", "What We Do in the Shadows", "Let the Right One In", "The Book of Life", "The Passion of the Christ", "Inside Out 2", "X-Men: Days of Future Past", "The Girl with the Dragon Tattoo", "Captain Phillips", "The Wrestler", "True Romance", "The Danish Girl", "Donnie Brasco", "Training Day", "Zodiac", "The Crow", "Evil Dead II", "We Need to Talk About Kevin", "The Tomorrow War", "Kung Fu Hustle", "First Blood", "Moulin Rouge!", "E.T. the Extra-Terrestrial", "Upgrade", "The Machinist", "Godzilla vs. Kong", "Sinners", "Rogue One: A Star Wars Story", "The Goonies", "Midnight in Paris", "Almost Famous", "The Birds", "Anatomy of a Fall", "The Great Beauty", "The Call of the Wild", "The Black Phone", "Escape from Alcatraz", "In Bruges", "Mission: Impossible - Dead Reckoning Part One", "Walk the Line", "Hercules", "Ghostbusters", "The Name of the Rose", "The Fugitive", "Back to the Future Part III", "Boyhood", "The Book Thief", "Carol", "Deadpool 2", "A Star Is Born", "The Wave", "The Bourne Identity", "Instant Family", "BlacKkKlansman"]


ARCHIVO_JSON = "peliculas_letterboxd.json"

PAUSA = 2  # segundos de espera entre películas

# Lista sin repetidos, respetando el orden
Titulos = list(dict.fromkeys(Titulos))

# Si ya existe el JSON de una ejecución anterior, se carga y se continúa por donde se quedó
# (cada película procesada deja exactamente un registro, así que su posición coincide con la de la lista)
try:
    with open(ARCHIVO_JSON, encoding="utf-8") as f:
        peliculas = json.load(f)
except Exception:
    peliculas = []

pendientes = Titulos[len(peliculas):]
print(f"{len(pendientes)} películas pendientes ({len(peliculas)} ya guardadas).")


# Utilizo el undetectec driver de selenium 
driver = uc.Chrome()

try:
    # 1. Entrar a Letterboxd
    driver.get("https://letterboxd.com/")
    time.sleep(2)

    # 2. Aceptar cookies (si aparece el banner de consentimiento)
    try:
        boton_aceptar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
        )
        boton_aceptar.click()
        time.sleep(2)
    except Exception:
        print("No apareció el banner de cookies o ya fue aceptado.")

    # 3. Recorrer la lista: buscar -> entrar en la entrada -> scrapear -> siguiente
    for i, busqueda in enumerate(pendientes, start=1):
        registro = {"titulo": None, "valoracion": None, "director": [], "actores": []} # Campos del json

        try:
            # Búsqueda en el buscador de la web , en vez de buscar botones si accedemos a /films/busqueda obtenemos la entrada de la pelicula
            #siendo más eficiente (código para limpiar la url de caracteres que puedan dar problemas usando IA )
            texto_busqueda = busqueda.replace("/", " ").replace("?", " ").replace("#", " ")
            driver.get(f"https://letterboxd.com/search/films/{texto_busqueda}/")

            selector_resultados = "h2.headline-2 span.film-title-wrapper > a" # Esto lo que hace es buscar el enlace de la pelicula 
                                                                               #en los resultados de la busqueda
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector_resultados))
                )
                resultados = driver.find_elements(By.CSS_SELECTOR, selector_resultados)[:5]
            except Exception:
                resultados = []  # la búsqueda no devolvió nada

            if resultados:
                # Preferimos el resultado cuyo título coincida exactamente (ignorando
                # mayúsculas y signos); si ninguno coincide, nos quedamos con el primero
                objetivo = "".join(c for c in busqueda.lower() if c.isalnum()) # Debe ser de tipo alfanumérico para evitar problemas con acentos, signos, etc.
                elegido = resultados[0]
                for r in resultados:
                    nombre = (r.get_attribute("textContent") or "").strip().lower()
                    if "".join(c for c in nombre if c.isalnum()) == objetivo:
                        elegido = r
                        break

                # El título del resultado sirve de respaldo si la ficha no tiene h1
                registro["titulo"] = (elegido.get_attribute("textContent") or "").strip() # Esto sirve para obtener el título de la película del resultado de la búsqueda y guardarlo en el registro

                #  Entrar en la ficha de la película 
                driver.get(elegido.get_attribute("href"))
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#film-page-wrapper"))
                )

                # Título
                h1 = driver.find_elements(By.CSS_SELECTOR, "h1.headline-1")
                if h1:
                    registro["titulo"] = (h1[0].get_attribute("textContent") or "").strip() # De momento empleamos una idea parecida al X-PATH , esto se cambiará por un selector CSS más robusto en el futuro

                # Valoración: el enlace con la media (ej. "3.8")
                for a in driver.find_elements(
                    By.CSS_SELECTOR, "a.average-rating, a[href$='/ratings/']"
                ):
                    valor = (a.get_attribute("textContent") or "").strip()
                    if valor.replace(".", "", 1).isdigit():
                        registro["valoracion"] = float(valor)
                        break

                # Director(es): se usa textContent porque la pestaña Crew está oculta
                for a in driver.find_elements(By.CSS_SELECTOR, "a[href^='/director/']"):
                    nombre = (a.get_attribute("textContent") or "").strip()
                    if nombre and nombre not in registro["director"]:
                        registro["director"].append(nombre)

                # Actores ("Show All..." no empieza por /actor/, así que se descarta solo)
                for a in driver.find_elements(By.CSS_SELECTOR, "a[href^='/actor/']"):
                    nombre = (a.get_attribute("textContent") or "").strip()
                    if nombre and nombre not in registro["actores"]:
                        registro["actores"].append(nombre)
                if MAX_ACTORES:
                    registro["actores"] = registro["actores"][:MAX_ACTORES]

                print(f"[{i}/{len(pendientes)}] {registro['titulo']} -> {registro['valoracion']}")
            else:
                print(f"[{i}/{len(pendientes)}] SIN RESULTADOS: {busqueda}")

        except Exception as e:
            print(f"[{i}/{len(pendientes)}] ERROR con '{busqueda}': {e}")

        #  Guarda en JSON tras cada película (también si falló, para mantener el orden) 
        peliculas.append(registro)
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(peliculas, f, ensure_ascii=False, indent=2)

        time.sleep(PAUSA)

finally:
    try:
        driver.quit()
    except OSError:
        pass
