import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("IGDB_CLIENT_ID")
client_secret = os.getenv("IGDB_CLIENT_SECRET")

videojuegos = [('The Legend of Zelda: Ocarina of Time', 1998), ('SoulCalibur', 1999), ('Super Mario Galaxy 2', 2010), ('Grand Theft Auto IV', 2008), ('Super Mario Galaxy', 2007), ('Grand Theft Auto V', 2013), ('The Legend of Zelda: Breath of the Wild', 2017), ('Perfect Dark', 2000), ("Tony Hawk's Pro Skater 3", 2001), ('Red Dead Redemption 2', 2018), ('Metroid Prime', 2002), ('Grand Theft Auto III', 2001), ('Super Mario Odyssey', 2017), ('Halo: Combat Evolved', 2001), ('NFL 2K1', 2000), ('Half-Life 2', 2004), ('BioShock', 2007), ('GoldenEye 007', 1997), ('Uncharted 2: Among Thieves', 2009), ('Resident Evil 4', 2005), ("Baldur's Gate 3", 2023), ('The Orange Box', 2007), ('Tekken 3', 1998), ('Mass Effect 2', 2010), ('The House in Fata Morgana - Dreams of the Revenants Edition -', 2021), ('Elden Ring', 2022), ('The Elder Scrolls V: Skyrim', 2011), ('Half-Life', 1998), ('The Legend of Zelda: Tears of the Kingdom', 2023), ('The Legend of Zelda: The Wind Waker', 2003), ('Gran Turismo', 1998), ('The Legend of Zelda: Ocarina of Time', 2026), ('Metal Gear Solid 2: Sons of Liberty', 2001), ('Grand Theft Auto Double Pack', 2003), ('Portal: Companion Collection', 2022), ("Baldur's Gate II: Shadows of Amn", 2000), ('Grand Theft Auto: San Andreas', 2004), ('The Legend of Zelda: Tears of the Kingdom - Nintendo Switch 2 Edition', 2025), ('Grand Theft Auto: Vice City', 2002), ('LittleBigPlanet', 2008), ("The Legend of Zelda Collector's Edition", 2003), ('Halo 2', 2004), ('Gran Turismo 3: A-Spec', 2001), ('The Legend of Zelda: A Link to the Past / Four Swords', 2002), ("The Legend of Zelda: Majora's Mask", 2000), ('The Last of Us', 2013), ('The Legend of Zelda: Twilight Princess', 2006), ('Hades II', 2025), ('Persona 5 Royal', 2020), ('The Last of Us Remastered', 2014), ('Red Dead Redemption', 2010), ('Portal 2', 2011), ('Astro Bot', 2024), ('Final Fantasy IX', 2000), ('God of War', 2018), ("Tony Hawk's Pro Skater 4", 2002), ('Elden Ring: Shadow of the Erdtree', 2024), ('Devil May Cry', 2001), ('Batman: Arkham City', 2011), ('Metroid Prime Remastered', 2023), ('The Legend of Zelda: Ocarina of Time 3D', 2011), ('Chrono Cross', 2000), ('Gears of War', 2006), ('The Elder Scrolls IV: Oblivion', 2006), ("Sid Meier's Civilization II", 1996), ('Quake', 1996), ('Metaphor: ReFantazio', 2024), ('Call of Duty 4: Modern Warfare', 2007), ('BioShock Infinite', 2013), ('Halo 3', 2007), ('Ninja Gaiden Black', 2005), ('Metal Gear Solid', 1998), ('Grim Fandango', 1998), ('Jet Set Radio', 2000), ('Super Mario Advance 4: Super Mario Bros. 3', 2003), ("Tom Clancy's Splinter Cell: Chaos Theory", 2005), ('God of War: Ragnarok', 2022), ('Resident Evil Code: Veronica', 2000), ('Burnout 3: Takedown', 2004), ('Diablo', 1996), ('Metal Gear Solid 3: Subsistence', 2006), ('Call of Duty: Modern Warfare 2', 2009), ('Metal Gear Solid 4: Guns of the Patriots', 2008), ('God of War', 2005), ('Star Wars: Knights of the Old Republic', 2003), ("Sid Meier's Civilization IV", 2005), ('Super Mario 64', 1996), ('Virtua Fighter 4', 2002), ('Super Smash Bros. Brawl', 2008), ('Gran Turismo 2', 1999), ("Tom Clancy's Splinter Cell: Pandora Tomorrow", 2004), ('Grand Theft Auto: Chinatown Wars', 2009), ('Pac-Man Championship Edition DX', 2010), ('Half-Life: Alyx', 2020), ('Divinity: Original Sin II', 2017), ('Braid', 2008), ('Super Mario 3D World', 2013), ('Starcraft II: Wings of Liberty', 2010), ('SSX', 2000), ('Street Fighter IV', 2009), ('Minecraft', 2011), ('Persona 4 Golden', 2012), ('Persona 5', 2017), ('Quake III Arena', 2000), ("Tom Clancy's Splinter Cell", 2002), ('Homeworld', 1999), ('SSX 3', 2003), ('Okami', 2006), ('Fallout 3', 2008), ('Pro Evolution Soccer 2', 2003), ('SoulCalibur II', 2003), ('Mass Effect 3', 2012), ('Metal Gear Solid V: The Phantom Pain', 2015), ('Skies of Arcadia', 2000), ('The Legend of Zelda: Skyward Sword', 2011), ('Mario Kart: Super Circuit', 2001), ('Rock Band 3', 2010), ('NBA 2K1', 2000), ('Viewtiful Joe', 2003), ('Hades', 2020), ('Resident Evil 4', 2023), ('Virtua Fighter 4: Evolution', 2003), ("Uncharted 4: A Thief's End", 2016), ('Super Smash Bros. Ultimate', 2018), ('Resident Evil 2: Deluxe Edition', 2026), ('Paper Mario', 2001), ('Wipeout XL', 1996), ('INSIDE', 2016), ('Flipnote Studio', 2009), ('World Soccer Winning Eleven 7 International', 2004), ('The Witcher 3: Wild Hunt - Remastered', 2026), ('Clair Obscur: Expedition 33', 2025), ('Forza Horizon 4', 2018), ('SSX Tricky', 2001), ("Uncharted 3: Drake's Deception", 2011), ('Final Fantasy VII Rebirth', 2024), ('Rock Band', 2007), ('Super Mario Bros. Wonder', 2023), ('Xenoblade Chronicles 3: Expansion Pass Wave 4 - Future Redeemed', 2023), ('Bloodborne', 2015), ("Eternal Darkness: Sanity's Requiem", 2002), ('Warcraft III: Reign of Chaos', 2002), ('Banjo-Kazooie', 1998), ("Sid Meier's Gettysburg!", 1997), ('Celeste', 2018), ('Forza Motorsport', 2005), ('Forza Horizon 5', 2021), ('Vagrant Story', 2000), ('Advance Wars', 2001), ('Blue Prince', 2025), ('Sektori', 2026), ('Final Fantasy XII', 2006), ('The Witcher 3: Wild Hunt', 2015), ('Super Mario World: Super Mario Advance 2', 2002), ('Super Smash Bros. Melee', 2001), ('Street Fighter 6', 2023), ('Virtua Tennis', 2000), ('Rome: Total War', 2004), ('Forza Motorsport 3', 2009), ("Demon's Souls", 2020), ('Undertale', 2015), ('Batman: Arkham Asylum', 2009), ('Super Mario Sunshine', 2002), ("Tony Hawk's Pro Skater", 1999), ('Thief: The Dark Project', 1998), ('Fire Emblem: Awakening', 2013), ('Final Fantasy X', 2001), ('Wave Race 64', 1996), ("Sid Meier's Alpha Centauri", 1999), ('Divinity: Original Sin II - Definitive Edition', 2018), ('Galactic Civilizations II: Twilight of the Arnor', 2008), ('Guitar Hero II', 2006), ('Final Fantasy VII', 1997), ('Chrono Trigger', 2008), ('Final Fantasy XIV: Endwalker', 2021), ('Journey', 2012), ("Conker's Bad Fur Day", 2001), ('Mario Kart 8 Deluxe', 2017), ('Metroid Prime 2: Echoes', 2004), ('Metroid Fusion', 2002), ('The Witcher 3: Wild Hunt - Blood and Wine', 2016), ('Final Fantasy VI', 2007), ('Rayman Legends', 2013), ('UFO 50', 2024), ('Medal of Honor: Allied Assault', 2002), ('Myth: The Fallen Lords', 1997), ('Microsoft Flight Simulator', 2020), ('Guitar Hero', 2005), ('Metroid Prime Trilogy', 2009), ("Baldur's Gate", 1998), ('Overwatch', 2016), ('Big Walk', 2026), ("Klonoa 2: Lunatea's Veil", 2001), ('Mario Tennis', 2000), ('Colony Wars', 1997), ('Ratchet & Clank: Up Your Arsenal', 2004), ('Resident Evil (Remake)', 2002), ('Metal Gear Solid 3: Snake Eater', 2004), ('Twisted Metal: Black', 2001), ('Spyro: Year of the Dragon', 2000), ('Tomb Raider', 1996), ('Forza Horizon 3', 2016), ('Dwarf Fortress', 2006), ('Kentucky Route Zero - Act III', 2014), ('Crysis', 2007), ('Ninja Gaiden', 2004), ('DOA2: Hardcore', 2000), ('MLB 10: The Show', 2010), ("Yoshi's Island: Super Mario Advance 3", 2002), ('Star Wars Jedi Knight: Dark Forces II', 1997), ('ESPN NFL Football', 2003), ('Halo: Reach', 2010), ('Galactic Civilizations II: Dark Avatar', 2007), ('Mass Effect', 2007), ('The Operative: No One Lives Forever', 2000), ('Resident Evil 3: Nemesis', 1999), ('Forza Motorsport 4', 2011), ('Resident Evil', 1996), ('Crusader Kings III', 2020), ('Split Fiction', 2025), ('Planescape: Torment', 1999), ('Neverwinter Nights', 2002), ('Castlevania: Aria of Sorrow', 2003), ('Legacy of Kain: Soul Reaver', 1999), ('Golden Sun', 2001), ('DOOM: The Dark Ages - Revelations', 2026), ('Disco Elysium', 2019), ('World Soccer Winning Eleven 8 International', 2005), ('NieR: Automata - Game of the YoRHa Edition', 2019), ('Castlevania: Circle of the Moon', 2001), ('Donkey Kong Bananza', 2025), ('Satisfactory', 2024), ('Dark Souls II', 2014), ('Shovel Knight: Treasure Trove', 2017), ('Mario Golf', 1999), ('Crash Bandicoot: Warped', 1998), ('Mario Kart DS', 2005), ("Assassin's Creed II", 2009), ('Animal Well', 2024), ('Balatro', 2024), ('Animal Crossing: New Horizons', 2020), ('Final Fantasy XIV: Shadowbringers', 2019), ('Forza Horizon 6', 2026), ('World of Warcraft: Cataclysm', 2010), ('Bayonetta', 2010), ('Diablo III: Ultimate Evil Edition', 2014), ('ICO', 2001), ("Tom Clancy's Ghost Recon Advanced Warfighter", 2006), ('Mario & Luigi: Superstar Saga', 2003), ('Hollow Knight: Silksong', 2025), ('Syphon Filter', 1999), ('Ape Escape', 1999), ("Tony Hawk's Underground", 2003), ("Mario & Luigi: Bowser's Inside Story", 2009), ('Trials Evolution', 2012), ('Grand Theft Auto IV: The Lost and Damned', 2009), ('FIFA Soccer 12', 2011), ('Factorio', 2020), ('Black & White', 2001), ('Ratchet & Clank: Going Commando', 2003), ('FIFA Soccer 10', 2009), ('Portal', 2007), ('The Legend of Zelda: Phantom Hourglass', 2007), ('Dance Dance Revolution', 2001), ('Jack Jeanne', 2023), ('Advance Wars: Dual Strike', 2005), ('MLB 11: The Show', 2011), ('NieR: Automata - Become as Gods Edition', 2018), ('Jak and Daxter: The Precursor Legacy', 2001), ('Star Wars Rogue Leader: Rogue Squadron II', 2001), ('Deus Ex', 2000), ('Donkey Kong 64', 1999), ("Stephen's Sausage Roll", 2016), ('Tsukihime: A Piece of Blue Glass Moon', 2024), ('Panzer Dragoon Orta', 2003), ('Portal: Still Alive', 2008), ('Half-Life 2: Episode Two', 2007), ('Elden Ring: Tarnished Edition', 2026), ('Shin Megami Tensei: Persona 4', 2008), ('Hollow Knight', 2018), ('MLB 09: The Show', 2009), ('Blast Corps', 1997), ('WWF SmackDown! 2: Know Your Role', 2000), ("Sid Meier's Civilization III", 2001), ('VIDEOVERSE', 2023), ('LIMBO', 2010), ('Silent Hunter III', 2005), ('Chained Echoes', 2022), ('Super Meat Boy', 2010), ('Okami HD', 2012), ('Geometry Wars: Retro Evolved 2', 2008), ("Sid Meier's Civilization V", 2010), ('Falcon 4.0: Allied Force', 2005), ('The Stanley Parable: Ultra Deluxe', 2022), ('Metroid Prime 3: Corruption', 2007), ('Monster Hunter: World', 2018), ('Pushmo', 2011), ('Freedom Force', 2002), ('FIFA Soccer 13', 2012), ('and Roger', 2026), ('Sekiro: Shadows Die Twice', 2019), ('Tekken 8', 2024), ('Chicory: A Colorful Tale', 2021), ('Total War: Shogun 2', 2011), ('Empire: Total War', 2009), ('Beetle Adventure Racing', 1999), ('Final Fantasy VIII', 1999), ('Kentucky Route Zero - Act IV', 2016), ('Astro Bot Rescue Mission', 2018), ('Command & Conquer: Red Alert', 1996), ('Star Wars Jedi Knight II: Jedi Outcast', 2002), ('Wipeout HD Fury', 2009), ('Shin Megami Tensei: Persona 3 Portable', 2010), ("Schrodinger's Call", 2026), ('Neon White', 2022), ('Xenoblade Chronicles: Definitive Edition', 2020), ('Burnout Revenge', 2005), ('Dragon Quest VIII: Journey of the Cursed King', 2005), ('Metroid: Zero Mission', 2004), ('Pikmin', 2001), ('Sacrifice', 2000), ('Final Fantasy VII Remake Intergrade', 2026), ('Monster Hunter: World - Iceborne', 2019), ('Dead Cells', 2018), ('Resident Evil 4: Gold Edition', 2026), ('Rhythm Doctor', 2025), ('despelote', 2025), ('Rez', 2008), ("Demon's Souls", 2009), ('Castlevania: Symphony of the Night', 2007), ('Fable II', 2008), ('Rez Infinite', 2016), ('Final Fantasy Chronicles', 2001), ('Fallout', 1997), ('Valheim', 2026), ('Pizza Tower', 2023), ('The Talos Principle: Reawakened', 2025), ("Assassin's Creed: Brotherhood", 2010), ('Left 4 Dead', 2008), ('Dark Souls III', 2016), ('Phantasy Star Online', 2001), ('NASCAR Racing 2002 Season', 2002), ('Jade Empire', 2005), ('Gunstar Heroes', 2015), ('Dark Souls', 2011), ('Pokemon Pokopia', 2026), ('Need for Speed: Hot Pursuit 2', 2002), ('Grand Theft Auto IV: The Ballad of Gay Tony', 2009), ('Kynseed', 2022), ("Thank Goodness You're Here!", 2024), ('Homeworld: Cataclysm', 2000), ('Combat Mission: Barbarossa to Berlin', 2002), ('Cyberpunk 2077: Phantom Liberty', 2023), ('Tetris Effect', 2018), ('Fez', 2012), ('Dead Space', 2023), ('Cave Story', 2010), ('Guild Wars', 2005), ('The Walking Dead: Episode 5 - No Time Left', 2012), ('Atari 50: The Anniversary Celebration', 2022), ("Fire Emblem: Fortune's Weave", 2026), ('World Soccer Winning Eleven 9', 2006), ('Ace Combat 04: Shattered Skies', 2001), ('Max Payne', 2001), ('Hollow Knight: Voidheart Edition', 2018), ('Fire Emblem: Three Houses', 2019), ('World in Conflict', 2007), ('NieR: Automata - The End of YoRHa Edition', 2022), ('Resident Evil Requiem', 2026), ('Castlevania: Dawn of Sorrow', 2005), ('NASCAR Racing 4', 2001), ('Far Cry', 2004), ('Horizon Forbidden West: Complete Edition', 2024), ('Nuclear Throne', 2015), ('Dead Space', 2008), ('Like a Dragon: Infinite Wealth', 2024), ('Desktop Explorer', 2026), ('Lone Echo', 2017), ('XCOM: Enemy Unknown', 2012), ('NASCAR Racing 2003 Season', 2003), ('Shin Megami Tensei: Persona 3 FES', 2008), ('Apex Legends', 2019), ('NORCO', 2022), ('Madden NFL 2003', 2002), ('The Legend of Zelda: Breath of the Wild - Nintendo Switch 2 Edition', 1998), ('Madden NFL 2002', 2001), ('Madden NFL 2004', 2003), ('Company of Heroes', 1998), ('The Last of Us Part II', 1998), ('Unreal Tournament 2004', 2004), ('God of War II', 1998), ('Gears of War 2', 1998), ('World of Warcraft', 2004), ('God of War III', 1998), ('NFL 2K3', 2010), ('NHL 2002', 2001), ('Prince of Persia: The Sands of Time', 1998), ('The Sims', 1998), ('Team Fortress 2', 2010), ('System Shock 2', 2010), ('ESPN NFL 2K5', 2010), ('Age of Empires II: The Age of Kings', 1998), ('Super Smash Bros. for Nintendo 3DS / Wii U', 2010), ('Medal of Honor', 1998), ('Rock Band 2', 2010), ('The ICO & Shadow of the Colossus Collection', 1998), ('Out of the Park Baseball 17', 1998), ('Madden NFL 2005', 2004), ('Against the Storm', 1998), ('LittleBigPlanet 2', 2010), ('Slay The Princess - The Pristine Cut', 1998), ('World of Warcraft: Wrath of the Lich King', 1998), ('I Was a Teenage Exocolonist', 2026), ('Madden NFL 2001', 2000), ('Bayonetta 2', 2010), ('IL-2 Sturmovik', 2010), ('FreeSpace 2', 2010), ('Dragon Quest XI S: Echoes of an Elusive Age - Definitive Edition', 1998), ('The Legend of Zelda: Ocarina of Time / Master Quest', 1998), ('NCAA Football 2003', 2002), ('God of War: Chains of Olympus', 1998), ('World of Warcraft: The Burning Crusade', 1998), ('Shadow of the Colossus', 1998), ('The Longest Journey', 1998), ("Tony Hawk's Pro Skater 2", 2010), ('Killzone 2', 2010), ('Battlefield 2', 2010), ('God of War Collection', 1998), ('Gears of War 3', 1998), ("No One Lives Forever 2: A Spy in H.A.R.M.'s Way", 2026), ('The Legend of Zelda: A Link Between Worlds', 1998), ('Resident Evil 2', 2010), ('Caves of Qud', 1998), ('Call of Duty', 1998), ('Project Gotham Racing 2', 2010), ('The Sims 2', 1998), ('World of Goo', 1998), ('Slay the Princess', 1998), ('Marvel vs. Capcom 2', 2010), ('NBA Street Vol. 2', 2010), ('The Legend of Zelda: The Wind Waker HD', 1998), ('NHL 2001', 2000), ("Marvel's Spider-Man 2", 2010), ('Mina the Hollower', 1998), ('NCAA Football 2002', 2001), ('Ori and the Will of the Wisps', 1998), ('Trails in the Sky 2nd Chapter', 1998), ('MVP Baseball 2004', 2004), ('The Last of Us Part II Remastered', 1998), ('DAVE THE DIVER', 1998), ('Mark of the Ninja', 1998), ('Dead Space 2', 2010), ('Pikmin 2', 2010), ('Super Mario 3D Land', 2010), ('Mario Kart 8 DLC Pack 2', 2010), ('Lost and Found Co.', 2026), ('Flight Simulator 2002', 2001), ('Dota 2', 2010), ('TimeSplitters 2', 1998), ('Guild Wars 2', 2010), ('Forza Motorsport 2', 2010), ('Into the Breach', 1998), ('GTR 2', 2010), ('Bayonetta + Bayonetta 2', 2010), ('NBA 2K12', 2010), ('The Witcher 3: Wild Hunt - Hearts of Stone', 1998), ('Halo 2 Multiplayer Map Pack', 2010), ('Borderlands 2', 2010), ('Call of Duty 2', 1998), ("The Legend of Zelda: Majora's Mask 3D", 1998), ('Age of Mythology', 1998), ('Wipeout 3', 2001), ('Tiger Woods PGA Tour 2004', 2003), ('The Walking Dead: A Telltale Games Series', 1998), ('Pillars of Eternity', 1998), ('NHL 2K3', 2010), ('Left 4 Dead 2', 2010), ('Worldwide Soccer Manager 2005', 2004), ('Slay the Spire', 1998), ('Titanfall 2', 2010), ('NBA 2K3', 2010), ('Tekken 2', 2010), ('Xenoblade Chronicles 3', 2001), ('F-Zero GX', 2021), ("Super Mario 3D World + Bowser's Fury", 2010), ('NBA Street V3', 2001), ('The Legend of Zelda: The Minish Cap', 1998), ('NCAA Football 2004', 2003), ('The Seance of Blake Manor', 1998), ('Football Manager Handheld', 2005), ('Streets of Rage 2', 1998), ('Out of the Park Baseball 15', 1998), ('Quake II - Enhanced Edition', 2001), ('Destiny 2: The Final Shape', 1998), ('Death Stranding 2: On The Beach', 1998), ('Cuphead in the Delicious Last Course', 1998), ('Rise of Nations', 1998), ('Descent 3', 2001), ('The Curse of Monkey Island', 1998), ('World Series Baseball 2K3', 2010)]

url_token = "https://id.twitch.tv/oauth2/token"

url = "https://api.igdb.com/v4/games"

datos = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

respuesta = requests.post(url_token, data=datos)
respuesta.raise_for_status()

token = respuesta.json()["access_token"]

headers = {
    "Client-ID": client_id,
    "Authorization": "Bearer " + token
}

alternativas = {"The Legend of Zelda: A Link to the Past / Four Swords": "The Legend of Zelda: A Link to the Past & Four Swords", "Star Wars Rogue Leader: Rogue Squadron II": "Star Wars: Rogue Squadron II - Rogue Leader", "Beetle Adventure Racing": "Beetle Adventure Racing!", "Schrodinger's Call": "Schrödinger's Call", "The Walking Dead: Episode 5 - No Time Left": "The Walking Dead: Season One - Episode 5: No Time Left", "The Legend of Zelda: Ocarina of Time / Master Quest": "The Legend of Zelda: Ocarina of Time - Master Quest", "Marvel vs. Capcom 2": "Marvel vs. Capcom 2: New Age of Heroes", "Flight Simulator 2002": "Microsoft Flight Simulator 2002", "GTR 2": "GTR 2: FIA GT Racing Game", "Worldwide Soccer Manager 2005": "Football Manager 2005", "The Seance of Blake Manor": "The Séance of Blake Manor", "Cuphead in the Delicious Last Course": "Cuphead & The Delicious Last Course", "DOA2: Hardcore": "Dead or Alive 2: Hardcore", "Kentucky Route Zero - Act III": "Kentucky Route Zero: Act III", "Kentucky Route Zero - Act IV": "Kentucky Route Zero: Act IV", "Grand Theft Auto Double Pack": "Grand Theft Auto: Double Pack", "Xenoblade Chronicles 3: Expansion Pass Wave 4 - Future Redeemed": "Xenoblade Chronicles 3: Future Redeemed"}

ids_fijos = {("The Legend of Zelda: Ocarina of Time", 1998): 1029, ("The Legend of Zelda: Ocarina of Time", 2026): 405460, ("God of War", 2005): 549, ("God of War", 2018): 19560, ("Resident Evil 4", 2005): 974, ("Resident Evil 4", 2023): 132181, ("Dead Space", 2008): 37, ("Dead Space", 2023): 159119, ("Resident Evil", 1996): 424, ("Resident Evil (Remake)", 2002): 24869, ("Demon's Souls", 2020): 134606, ("The House in Fata Morgana - Dreams of the Revenants Edition -", 2021): 119577, ("The Legend of Zelda: Tears of the Kingdom - Nintendo Switch 2 Edition", 2025): 338073, ("Divinity: Original Sin II - Definitive Edition", 2018): 103337, ("Grand Theft Auto Double Pack", 2003): 119155, ("Portal: Companion Collection", 2022): 191406}

#Inicio código generado con IA
def normalizar(texto):
    texto = texto.lower()
    texto = texto.replace("é", "e")
    texto = texto.replace("ö", "o")
    texto = texto.replace(":", "")
    texto = texto.replace("-", "")
    texto = texto.replace("'", "")
    texto = texto.replace(".", "")
    texto = texto.replace("&", "and")
    return " ".join(texto.split())
#Final código generado con IA

resultados_igdb = []

for numero, (nombre, anio) in enumerate(videojuegos, 1):

    campos = "id,name,alternative_names.name,rating,rating_count,game_type.type,themes.name,game_modes.name,player_perspectives.name"
    
    if (nombre, anio) in ids_fijos:

        id_igdb = ids_fijos[(nombre, anio)]

        consulta = (
            "fields " + campos + "; "
            "where id = " + str(id_igdb) + "; "
            "limit 1;"
        )

    else:

        titulo = alternativas.get(nombre, nombre)
        titulo = titulo.replace('"', '\\"')

        consulta = (
            'search "' + titulo + '"; '
            "fields " + campos + "; "
            "limit 100;"
        )

    try:
        respuesta = requests.post(url, headers=headers, data=consulta, timeout=30)
        respuesta.raise_for_status()
        candidatos = respuesta.json()

    except requests.RequestException as error:
        print("Error:", nombre, error)
        candidatos = []

    mejor = None

    if (nombre, anio) in ids_fijos:

        if len(candidatos)>0:
            mejor = candidatos[0]

    else:

        votos_maximos = -1

        for juego in candidatos:

            coincide = False
            titulo = alternativas.get(nombre, nombre)

            if normalizar(juego["name"]) == normalizar(titulo):
                coincide = True

            #Inicio bloque generado por IA
            for alternativo in juego.get("alternative_names", []):

                if normalizar(alternativo["name"]) == normalizar(titulo):
                    coincide = True

            if coincide is True:

                votos = juego.get("rating_count") or 0

                if mejor is None:
                    mejor = juego

                if juego.get("rating") is not None and votos > votos_maximos:
                    mejor = juego
                    votos_maximos = votos
            #Final bloque generado por IA
    resultado = {
        "nombre": nombre,
        "user_score": None,
        "category": None,
        "themes": [],
        "game_modes": [],
        "player_perspective": []
    }

    if mejor is not None:

        if mejor.get("rating") is not None:
            resultado["user_score"] = round(mejor["rating"], 2)

        if mejor.get("game_type") is not None:
            resultado["category"] = mejor["game_type"]["type"]

        for tema in mejor.get("themes", []):
            resultado["themes"].append(tema["name"])

        for modo in mejor.get("game_modes", []):
            resultado["game_modes"].append(modo["name"])

        for perspectiva in mejor.get("player_perspectives", []):
            resultado["player_perspective"].append(perspectiva["name"])

    resultados_igdb.append(resultado)

    print(numero, "/", len(videojuegos), "-", nombre, "-", resultado["user_score"])


#Inicio código generado por IA
with open("videojuegos_igdb.json", "w", encoding="utf-8") as archivo:
    json.dump(resultados_igdb, archivo, ensure_ascii=False, indent=4)
#Final código generado por IA

con_valoracion = 0

for juego in resultados_igdb:

    if juego["user_score"] is not None:
        con_valoracion += 1

print("Total:", len(resultados_igdb))
print("Con valoración:", con_valoracion)
print("Sin valoración:", len(resultados_igdb) - con_valoracion)
