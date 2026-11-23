import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TMDB_TOKEN")

lista = [['Breaking Bad', 'Breaking Bad', 2008], ['Sutîru Bôru Ran JoJo no Kimyô na Bôken', "Steel Ball Run: JoJo's Bizarre Adventure", 2026], ['The Wire', 'The Wire', 2002], ['Avatar: The Last Airbender', 'Avatar: La leyenda de Aang', 2005], ['Game of Thrones', 'Game of Thrones', 2011], ['The Sopranos', 'Los Soprano', 1999], ['Bluey', 'Bluey', 2018], ['Sapne vs Everyone', 'Sapne Vs Everyone', 2023], ['The World at War', 'El Mundo en Guerra', 1973], ['Our Planet', 'Nuestro planeta', 2019], ['BB Ki Vines', 'BB Ki Vines', 2015], ['Shingeki no kyojin', 'Attack on Titan', 2013], ['The Chosen', 'The Chosen', 2017], ['Hagane no renkinjutsushi', 'Fullmetal Alchemist: Brotherhood', 2009], ['Gullak', 'Gullak', 2019], ['Aspirants', 'Aspirants', 2021], ['The Legend of Hanuman', 'The Legend of Hanuman', 2021], ['Vratice se rode', 'Vratice se rode', 2007], ['The Filthy Frank Show', 'The Filthy Frank Show', 2011], ['Dexter: Resurrection', 'Dexter: Resurrección', 2025], ['Better Call Saul', 'Better Call Saul', 2015], ['The Office', 'La oficina', 2005], ['One Piece: Wan pîsu', 'One Piece', 1999], ['Rick and Morty', 'Rick & Morty', 2013], ['Bleach: Sennen Kessen-hen', 'Bleach: Thousand-Year Blood War', 2022], ['The Twilight Zone', 'La dimensión desconocida', 1959], ['Sherlock', 'Sherlock', 2010], ['Arcane: League of Legends', 'Arcane', 2021], ['Hunter x Hunter', 'Hunter X Hunter', 2011], ['Taskmaster', 'Taskmaster', 2015], ['Batman: The Animated Series', 'Batman: La serie animada', 1992], ['Only Fools and Horses', 'Only fools and horses', 1981], ["Clarkson's Farm", 'La Granja de Clarkson', 2021], ['Gibi', 'Gibi', 2021], ['Panchayat', 'Panchayat', 2020], ['Eungdaphara 1988', 'Eung-dab-ha-ra 1988', 2015], ['Naui ajusshi', 'Mi Señor', 2018], ['Ramayan', 'Ramayan', 1987], ['Critical Role', 'Critical Role', 2015], ['Kota Factory', 'La fábrica de Kota', 2019], ['TVF Pitchers', 'TVF Pitchers', 2015], ['Leyla ile Mecnun', 'Leyla ile Mecnun', 2011], ['Sandeep Bhaiya', 'Sandeep Bhaiya', 2023], ['Koombiyo', 'Koombiyo', 2017], ['The Pitt', 'The Pitt', 2025], ['The West Wing', 'The West Wing', 1999], ['Nathan for You', 'Nathan for You', 2013], ['Vinland Saga', 'Vinland Saga', 2019], ['Death Note: Desu nôto', 'Death Note', 2006], ['Sôsô no Furîren', 'Frieren: Más allá del final del viaje', 2023], ['Gravity Falls', 'Gravity Falls: Un verano de misterios', 2012], ['Firefly', 'Firefly', 2002], ['Kaubôi bibappu', 'Cowboy Bebop', 1998], ['Sahsiyet', 'Sahsiyet', 2018], ['Still Game', 'Still Game', 2002], ['Pod prikritie', 'Undercover', 2011], ['Omar', 'Omar', 2012], ['Mahabharat', 'Mahabharat', 1988], ['Yeh Meri Family', 'Yeh Meri Family', 2018], ['Tash Ma Tash', 'Tash Ma Tash', 1993], ['NCR Days', 'NCR Days', 2022], ['True Detective', 'True Detective', 2014], ['Friends', 'Friends', 1994], ['Succession', 'Succession', 2018], ["It's Always Sunny in Philadelphia", 'Siempre hay sol en Filadelfia', 2005], ['Fargo', 'Fargo', 2014], ['Seinfeld', 'Seinfeld', 1989], ['BoJack Horseman', 'BoJack Horseman', 2014], ['Curb Your Enthusiasm', 'El show de Larry David', 2000], ['Monster', 'Monster', 2004], ['Kenpuu Denki Berserk', 'Berserk', 1997], ['Steins;Gate', 'Steins;Gate', 2011], ['Dragon Ball Z', 'Dragon Ball Z', 1996], ['Fawlty Towers', 'Fawlty Towers', 1975], ['Hajime no Ippo', 'Hajime no ippo', 2000], ['Last Week Tonight with John Oliver', 'Last Week Tonight with John Oliver', 2014], ['Banjjagineun Woteomellon', 'Sparkling Watermelon', 2023], ['Dragon Ball Z: Doragon bôru zetto', 'Dragon Ball Z', 1989], ['Blackadder Goes Forth', 'Blackadder Goes Forth', 1989], ["Monty Python's Flying Circus", "Monty Python's Flying Circus", 1969], ['Re:Zero kara Hajimeru Isekai Seikatsu', 'Re Zero Kara Hajimeru Isekai Seikatsu - Shin Henshuu-ban', 2016], ["Chappelle's Show", "Chappelle's Show", 2003], ['Senke nad Balkanom', 'Senke nad Balkanom', 2017], ['Behzat Ç.', 'Behzat Ç.: Bir Ankara Polisiyesi', 2010], ["Mister Rogers' Neighborhood", "Mister Rogers' Neighborhood", 1968], ['Rocket Boys', 'Rocket Boys', 2022], ['Flames', 'Flames', 2018], ['Sarabhai V/S Sarabhai', 'Sarabhai V/S Sarabhai', 2004], ['Ted Lasso', 'Ted Lasso', 2020], ['South Park', 'South Park', 1997], ['Star Trek: The Next Generation', 'Viaje a las estrellas: La nueva generación', 1987], ['Black Mirror', 'Black Mirror', 2011], ['Dark', 'Dark', 2017], ['House M.D.', 'Dr. House', 2004], ['Mad Men', 'Mad Men', 2007], ['Peaky Blinders', 'Peaky Blinders', 2013], ['Twin Peaks', 'Twin Peaks', 1990], ['Heated Rivalry', 'Más que rivales', 2025], ['Invincible', 'Invincible', 2021], ['This Is Us', 'This is Us', 2016], ['Downton Abbey', 'Downton Abbey', 2010], ['Six Feet Under', 'Seis pies bajo tierra', 2001], ['Line of Duty', 'Line of Duty', 2012], ['Naruto: Shippûden', 'Naruto: Shippûden', 2007], ['Friday Night Lights', 'Friday Night Lights', 2006], ['Mr Inbetween', 'Mr Inbetween', 2018], ['Fleabag', 'Fleabag', 2016], ['Battlestar Galactica', 'Galáctica, estrella de combate', 2004], ['Narcos', 'Narcos', 2015], ['Rome', 'Roma', 2005], ['The Shield', 'El escudo', 2002], ['Adventure Time', 'Hora de Aventura', 2010], ['Blue Eye Samurai', 'Samurái de ojos azules', 2023], ['Kôdo Giasu: Hangyaku no Rurûshu', 'Code Geass: Lelouch of the Rebellion', 2006], ['Oz', 'Oz', 1997], ["X-Men '97", "X-Men '97", 2024], ['Freaks and Geeks', 'Jóvenes y rebeldes', 1999], ['Gintama', 'Gintama', 2005], ['Le bureau des légendes', 'Le Bureau des Légendes', 2015], ['Peep Show', 'Peep Show', 2003], ['Hwan Hon', 'Alquimia de almas', 2022], ['How to with John Wilson', 'How to with John Wilson', 2020], ['Haikyû!!', 'Haikyuu!!', 2014], ['Homicide: Life on the Street', 'Homicide: Life on the Street', 1993], ['Dhindora', 'Dhindora', 2021], ['Top Gear', 'Top Gear', 2002], ['The Thick of It', 'The Thick of It', 2005], ['Justice League Unlimited', 'Liga de la Justicia Ilimitada', 2004], ['The Grand Tour', 'The Grand Tour', 2016], ['Miseuteo Shunshain', 'Miseuteo Shunshain', 2018], ['The Adventures of Sherlock Holmes', 'The Adventures of Sherlock Holmes', 1984], ['The Return of Sherlock Holmes', 'El regreso de Sherlock Holmes', 1986], ['Seulgiroun Euisasaenghal', 'Seulgiroun Euisasaenghal', 2020], ['El Chavo del Ocho', 'El Chavo del Ocho', 1972], ['Chen qing ling', 'The untamed', 2019], ['Umbre', 'Umbre', 2014], ['Mahabharat', 'Mahabharat', 2013], ['Halka', 'Halka', 2019], ['Harga', 'Harga', 2021], ['Pew News', 'Pew News', 2018], ['Dexter', 'Dexter', 2006], ['Stranger Things', 'Stranger Things', 2016], ['Severance', 'Severance', 2022], ['A Knight of the Seven Kingdoms', 'A Knight of the Seven Kingdoms', 2026], ['Yellowstone', 'Yellowstone', 2018], ['The X Files', 'Los expedientes secretos X', 1993], ['The Simpsons', 'Los Simpson', 1989], ['Andor', 'Andor', 2022], ['Parks and Recreation', 'Parks and Recreation', 2009], ['The Crown', 'The Crown', 2016], ['JoJo no Kimyô na Bôken', 'Golden Wind', 2012], ['Shogun', 'Shōgun', 2024], ['Daredevil', 'Daredevil', 2015], ['Mindhunter', 'Midhunter', 2017], ['Justified', 'Justified: La ley de Raylan', 2010], ['Deadwood', 'Deadwood', 2004], ['Poirot', 'Poirot', 1989], ['The Mandalorian', 'The Mandalorian', 2019], ['Kusuriya no hitorigoto', 'Los diarios de la boticaria', 2023], ['House of Cards', 'House of Cards', 2013], ['Arrested Development', 'Sacrificios de familia', 2003], ['All Creatures Great & Small', 'All Creatures Great & Small', 2020], ['The Newsroom', 'The Newsroom', 2012], ['Call the Midwife', 'Llamen a la partera', 2012], ['The Marvelous Mrs. Maisel', 'La maravillosa Sra. Maisel', 2017], ['One Punch Man: Wanpanman', 'One Punch Man', 2015], ['Atlanta', 'Atlanta', 2016], ['Shoresy', 'Shoresy', 2022], ['Detectorists', 'Detectorists', 2014], ['The Great British Bake Off', 'The Great British Bake Off', 2010], ['Archer', 'Archer', 2009], ['Regular Show', 'Un show más', 2010], ['Bron/Broen', 'Bron/Broen', 2011], ['Gomorra', 'Gomorra: La serie', 2014], ['Endeavour', 'Endeavour', 2012], ['Wentworth', 'Wentworth', 2013], ['Anne with an E', 'Anne with an E', 2017], ["Foyle's War", "Foyle's War", 2002], ['Mauseu', 'Mauseu', 2021], ['Mr. Bean', 'Mr. Bean', 1990], ['Shigatsu wa kimi no uso', 'Shigatsu wa kimi no uso', 2014], ["L'amica geniale", 'La amiga estupenda', 2018], ['Primal', 'Primal', 2019], ['The Owl House', 'The Owl House', 2020], ['Young Justice', 'Justicia Joven', 2010], ['The Family Man', 'Hombre de familia', 2019], ['Pose', 'Pose', 2018], ['Hilda', 'Hilda', 2018], ['Adventure Time: Fionna and Cake', 'Hora de aventura con Fionna & Cake', 2023], ['QI', 'QI', 2003], ['Father Ted', 'Father Ted', 1995], ['Dalui Yeonin - Bobogyungsim Ryeo', 'Moon Lovers: Scarlet Heart Ryeo', 2016], ['Ezel', 'Ezel', 2009], ['Blackadder II', 'Blackadder II', 1986], ['The Venture Bros.', 'The Venture Bros.', 2003], ['Yes Minister', 'Yes Minister', 1980], ['Blackadder the Third', 'Blackadder the Third', 1987], ['Mystery Science Theater 3000', 'Mystery Science Theater 3000', 1988], ['Through the Wormhole', 'Secretos del universo', 2010], ['Mind Your Language', 'Mind Your Language', 1977], ['Yes, Prime Minister', 'Yes, Prime Minister', 1986], ["I'm Alan Partridge", "I'm Alan Partridge", 1997], ['Permanent Roommates', 'Permanent Roommates', 2014], ['Brass Eye', 'Brass Eye', 1997], ['Hunter x Hunter', 'Cazador X', 1999], ['Very Parivarik', 'Very Parivarik', 2024], ['Merlí', 'Merlí', 2015], ['Campus Diaries', 'Campus Diaries', 2022], ['Avrupa Yakasi', 'Avrupa Yakasi', 2004], ['Kardes Payi', 'Kardes Payi', 2014], ['Isler Güçler', 'Isler Güçler', 2012], ['Content Cop', 'Content Cop', 2015], ['The Boys', 'The Boys', 2019], ['The Bear', 'El oso', 2022], ['Modern Family', 'Modern Family', 2009], ['The Rehearsal', 'El ensayo', 2022], ['Shameless', 'Shameless', 2011], ['Jujutsu Kaisen', 'Jujutsu Kaisen', 2020], ['Sons of Anarchy', 'Los indomables', 2008], ['Vikings', 'Vikingos', 2013], ['Doctor Who', 'Doctor Who', 2005], ['Hannibal', 'Hannibal', 2013], ['Mr. Robot', 'Mr. Robot', 2015], ['Community', 'Community', 2009], ['The Expanse', 'The Expanse', 2015], ['Schitt$ Creek', "Schitt's Creek", 2015], ['Boardwalk Empire', 'Boardwalk Empire. El Imperio del Contrabando', 2010], ['Kimetsu no Yaiba', 'Demon Slayer: Kimetsu no Yaiba', 2019], ['What We Do in the Shadows', 'What We Do in the Shadows', 2019], ['Ore dake Reberu Appu na Ken', 'I Level Up Alone', 2024], ['The Last Kingdom', 'The Last Kingdom', 2015], ['Snowfall', 'Snowfall', 2017], ['Twin Peaks', 'Twin Peaks', 2017], ['M*A*S*H', 'M.A.S.H.', 1972], ['Bosch', 'Bosch', 2014], ['Boston Legal', 'Boston Legal', 2004], ['Happy Valley', 'Happy Valley', 2014], ['Futurama', 'Futurama', 1999], ['Silicon Valley', 'Silicon Valley', 2014], ['Letterkenny', 'Letterkenny', 2016], ['Derry Girls', 'Derry Girls', 2018], ['Star Wars: The Clone Wars', 'Star Wars: La guerra de los clones', 2008], ['The IT Crowd', 'The IT Crowd', 2006], ['Mob Psycho 100', 'Mob Psycho 100', 2016], ['Shinseiki Evangelion', 'Neon Genesis Evangelion', 1995], ['Inside No. 9', 'Inside No. 9', 2014], ['Pantheon', 'Panteón', 2022], ['Southland', 'Southland', 2009], ['Star Wars: Maul - Shadow Lord', 'Star Wars: Maul - Lord de las sombras', 2026], ['The Office', 'The Office', 2001], ['Heartstopper', 'Heartstopper', 2022], ['Smiling Friends', 'Smiling Friends', 2020], ['Common Side Effects', 'Common Side Effects', 2024], ['The Boondocks', 'Los Boondocks', 2005], ['Trailer Park Boys', 'Trailer Park Boys', 2001], ['Guimi Zhi Zhu', 'Señor de los Misterios', 2025], ['The Jinx: The Life and Deaths of Robert Durst', 'La Maldición', 2015], ["Kaguya-sama wa kokurasetai ~ Tensai tachi no ren'ai zunô sen ~", "Kaguya-sama wa kokurasetai ~ Tensai tachi no ren'ai zunô sen ~", 2019], ['Samurai Jack', 'Samurai Jack', 2001], ['Samurai Chanpurû', 'Samurai Champloo', 2004], ['Dragon Ball', 'Dragon Ball', 1995], ['Hagane no renkinjutsushi', 'Fullmetal Alchemist', 2003], ['Justice League', 'Liga de la justicia', 2001], ['Kingdom', 'Kingdom', 2014], ['Dragon Ball: Doragon bôru', 'Dragon Ball', 1986], ['Nana', 'Nana', 2006], ['Agui kkot', 'Flower of Evil', 2020], ['Alfred Hitchcock Presents', 'Alfred Hitchcock Presents', 1955], ['Flight of the Conchords', 'Flight of the Conchords', 2007], ['Furûtsu Basuketto', 'Fruits Basket', 2019], ['Impractical Jokers', 'Impractical Jokers', 2011], ['Spaced', 'Spaced', 1999], ['Staged', 'Staged', 2020], ['Sacred Games', 'Juegos sagrados', 2018], ['Mushishi', 'Mushishi', 2005], ['Making a Murderer', 'Making a Murderer', 2015], ['Louie', 'Louie', 2010], ['Coupling', 'Coupling', 2000], ['Tu Bian Ying Xiong X', 'To Be Hero X', 2025], ['I Love Lucy', 'Yo amo a Lucy', 1951], ['Meitantei Conan', 'Detective Conan', 1996], ['Cheolinwanghoo', 'Cheolinwanghoo', 2020], ['Skam', 'Skam', 2015], ['Yu yu hakusho', 'Los guerreros del más allá', 1992], ["RuPaul's Drag Race", "RuPaul's Drag Race", 2009], ['Queer as Folk', 'Queer as Folk', 2000], ['The Dick Van Dyke Show', 'The Dick Van Dyke Show', 1961], ['Whose Line Is It Anyway?', 'Whose Line Is It Anyway?', 1998], ['Rurôni Kenshin: Meiji kenkaku romantan', 'Samurái X', 1996], ['GTO', 'GTO: Great teacher Onizuka', 1999], ['Made in India: A Titan Story', 'Made in India: A Titan Story', 2026], ['The Eric Andre Show', 'The Eric Andre Show', 2012], ['The Larry Sanders Show', 'The Larry Sanders Show', 1992], ['Kôkaku Kidôtai Sutando Arôn Conpurekkusu', 'Kôkaku kidôtai: Stand Alone Complex', 2002], ['Please Like Me', 'Please Like Me', 2013], ["Chef's Table", "Chef's Table", 2015], ['Prens', 'El príncipe', 2023], ['The Bugs Bunny Show', 'Festival Bugs Bunny: El conejo de la suerte', 1960], ["RuPaul's Drag Race All Stars", "RuPaul's Drag Race All Stars", 2012], ['Special Ops', 'Special OPS', 2020], ['ImMATURE', 'ImMATURE', 2019], ['TVF Tripling', 'TVF Tripling', 2016], ['Bandish Bandits', 'Bandish Bandits', 2020], ['Hostel Daze', 'Hostel Daze', 2019], ['Broken But Beautiful', 'Broken But Beautiful', 2018], ['Queer Eye', 'Queer Eye', 2018], ['The Angry Video Game Nerd', 'The Angry Video Game Nerd', 2004], ['Sixer', 'Sixer', 2022], ['The Bugs Bunny/Road Runner Hour', 'The Bugs Bunny/Road Runner Hour', 1968], ['Shabhaye Barareh', 'Shabhaye Barareh', 2005], ['Lucky Guy', 'Lucky Guy', 2023], ['Slow Horses', 'Caballos lentos', 2022], ['Supernatural', 'Supernatural', 2005], ['Person of Interest', 'Vigilados', 2011], ['The Americans', 'The Americans', 2013], ['The Last of Us', 'The Last of Us', 2023], ['Ghosts', 'Ghosts', 2019], ['Suits', 'Suits', 2011], ['Banshee', 'Banshee', 2013], ['Star Trek', 'Viaje a las estrellas', 1966], ['Brooklyn Nine-Nine', 'Brooklyn Nine-Nine', 2013], ['The Punisher', 'The Punisher', 2017], ['Ozark', 'Ozark', 2017], ['Big Little Lies', 'Big Little Lies', 2017], ['Westworld', 'Westworld', 2016], ['Stargate SG-1', 'Stargate SG-1', 1997], ['Fringe', 'Fringe', 2008], ['Scrubs', 'Scrubs', 2001], ['Psych', 'Psych', 2006], ['Babylon Berlin', 'Babylon Berlin', 2017], ['24', '24', 2001], ['Spartacus', 'Spartacus', 2010], ['Veep', 'Veep', 2012], ['Heartland', 'Heartland', 2007], ['Naruto', 'Naruto', 2002], ['Love, Death & Robots', 'Love, Death & Robots', 2019], ['Cobra Kai', 'Cobra Kai', 2018], ['Entourage', 'Entourage', 2004], ['Unforgotten', 'Unforgotten', 2015], ['Chamgyoyuk', 'Así aprenderás', 2026], ['Top Boy', 'Top Boy', 2011], ['The Legend of Vox Machina', 'La leyenda de Vox Machina', 2022], ['Doc Martin', 'Doc Martin', 2004], ['Luther', 'Luther', 2010], ['Mirzapur', 'Mirzapur', 2018], ['Red Dwarf', 'Red Dwarf', 1988], ['After Life', 'After Life: Más allá de mi mujer', 2019], ['Warrior', 'Warrior', 2019], ['Babylon 5', 'Babilonia 5', 1993], ['Yakhanyeongung', 'Weak Hero Class 1', 2022], ['The Mighty Nein', 'The Mighty Nein', 2025], ['Pachinko', 'Pachinko', 2022], ['Doctor Who', 'Doctor Who', 1963], ['American Crime Story', 'American Crime Story', 2016], ['Ash vs Evil Dead', 'Ash contra el mal', 2015], ['The League of Gentlemen', 'The League of Gentlemen', 1999], ['Bosch: Legacy', 'Bosch: El Legado', 2022], ['Halt and Catch Fire', 'Halt and Catch Fire', 2014], ['The Amazing World of Gumball', 'El Increíble Mundo de Gumball', 2011], ['Bir Baskadir', 'Nos conocimos en Estambul', 2020], ['The Inbetweeners', 'The Inbetweeners', 2008], ['Utopia', 'Utopia', 2013], ['Love/Hate', 'Love/Hate', 2010], ['The Knick', 'The Knick', 2014], ['Northern Exposure', 'La última frontera', 1990], ['Binsenjo', 'Binsenjo', 2021], ['Broad City', 'Broad City', 2014], ['Yijae, Got Jookseummida', "Death's Game", 2023], ['The Andy Griffith Show', 'The Andy Griffith Show', 1960], ['Pushing Daisies', 'Pushing Daisies', 2007], ['Mubing', 'Moving', 2023], ['Brassic', 'Brassic', 2019], ['X-Men', 'X-Men', 1992], ['Black Books', 'Black Books', 2000], ['Forbrydelsen', 'Forbrydelsen', 2007], ['Spider-Man', 'Spider-Man', 1994], ['Borgen', 'Borgen', 2010], ['Last Tango in Halifax', 'Last Tango in Halifax', 2012], ['All in the Family', 'All in the Family', 1971], ['This Country', 'This Country', 2017], ['Steins;Gate 0', 'Steins;Gate 0', 2018], ['Carnivàle', 'Carnivàle', 2003], ['My So-Called Life', 'My So-Called Life', 1994], ['The Graham Norton Show', 'The Graham Norton Show', 2007], ['Sigeuneol', 'Sigeuneol', 2016], ['Trollhunters', 'Trollhunters', 2016], ['Hilleo', 'Hilleo', 2014], ['Formula 1: Drive to Survive', 'Formula 1: Drive to Survive', 2019], ['The New Batman Adventures', 'Las nuevas aventuras de Batman', 1997], ['Bimilui Soop', 'Stranger', 2017], ['The Dark Crystal: Age of Resistance', 'El cristal encantado: La era de la resistencia', 2019], ['Delhi Crime', 'Delhi Criminal', 2019], ['The Muppet Show', 'El show de los Muppets', 1976], ['Infinity Train', 'El tren infinito', 2019], ['The Spectacular Spider-Man', 'El espectacular Hombre Araña', 2008], ['Prehistoric Planet', 'Planeta prehistórico', 2022], ['The Prisoner', 'El prisionero', 1967], ['Invader ZIM', 'Invasor Zim', 2001], ['Whose Line Is It Anyway?', 'Whose Line Is It Anyway?', 2013], ['Mr. Show with Bob and David', 'Mr. Show with Bob and David', 1995], ['Jeeves & Wooster', 'Jeeves & Wooster', 1990], ['Asur: Welcome to Your Dark Side', 'Asur: Welcome to Your Dark Side', 2020], ['My Mad Fat Diary', 'My Mad Fat Diary', 2013], ["'Allo 'Allo!", "'Allo 'Allo!", 1982], ['The Kids in the Hall', 'The Kids in the Hall', 1988], ['Julie and the Phantoms', 'Julie and the Phantoms', 2020], ['Saint Seiya', 'Los caballeros del zodíaco', 1986], ['The Heroes', 'The Heroes', 2008], ['The Ricky Gervais Show', 'El show de Ricky Gervais', 2010], ['The Late Late Show with Craig Ferguson', 'The Late Late Show with Craig Ferguson', 2005], ['The Adventures of Pete & Pete', 'The Adventures of Pete & Pete', 1992], ['Red vs. Blue', 'Red vs. Blue', 2003], ['Mumbai Diaries', 'Mumbai Diaries', 2021], ['Stromberg', 'Stromberg', 2004], ['Top Gear', 'Top Gear', 1978], ['Yarin Yokmus Gibi', 'Como si no hubiera un mañana', 2024], ['The Colbert Report', 'The Colbert Report', 2005], ['MobLand', 'MobLand', 2025], ['Black Clover', 'Black Clover', 2017], ['Cyberpunk: Edgerunners', 'Cyberpunk: Edgerunners', 2022], ['Lost', 'Lost', 2004], ['The Leftovers', 'The Leftovers', 2014], ['Fallout', 'Fallout', 2024], ['Outlander', 'Outlander', 2014], ['Re:Zero kara Hajimeru Isekai Seikatsu', 'Re: Zero kara hajimeru isekai seikatsu', 2016], ['Homeland', 'Homeland', 2011], ['How I Met Your Mother', 'How I Met Your Mother. Cómo conocí a tu madre', 2005], ["The Handmaid's Tale", 'El cuento de la criada', 2017], ['Prison Break', 'Prison Break', 2005], ['Buffy the Vampire Slayer', 'Buffy, la cazavampiros', 1997], ['One Piece', 'One Piece', 2023], ['Hacks', 'Hacks', 2021], ['Columbo', 'Columbo', 1971], ['Rectify', 'Rectify', 2013], ['1923', '1923', 2022], ['Bleach', 'Bleach', 2004], ['Fauda', 'Fauda', 2015], ['The Good Wife', 'The Good Wife', 2009], ['The Legend of Korra', 'La leyenda de Korra', 2012], ['Broadchurch', 'Broadchurch', 2013], ['Barry', 'Barry', 2018], ['Shetland', 'Shetland', 2013], ['30 Rock', '30 Rock', 2006], ['The Other Bennet Sister', 'The Other Bennet Sister', 2026], ['Parenthood', 'Parenthood', 2010], ['Taboo', 'Taboo', 2017], ['The Killing', 'The Killing', 2011], ['Billions', 'Billions', 2016], ['Chainsaw Man', 'Chainsaw Man', 2022], ['Ray Donovan', 'Ray Donovan', 2013], ['Blue Mountain State', 'Blue Mountain State', 2010], ['Police Squad!', 'Police Squad!', 1982], ['Veronica Mars', 'Veronica Mars', 2004], ['Why Women Kill', 'Why Women Kill', 2019], ['Orphan Black', 'Orphan Black', 2013], ['Studio 60 on the Sunset Strip', 'Studio 60 on the Sunset Strip', 2006], ['Longmire', 'Longmire', 2012], ['Wayne', 'Wayne', 2019], ['Cien años de soledad', 'Cien años de soledad', 2024], ['Californication', 'Californication', 2007], ['Castlevania', 'Castlevania', 2017], ['Perry Mason', 'Perry Mason', 1957], ['Reservation Dogs', 'Reservation Dogs', 2021], ['Dandadan', 'Dandadan', 2024], ['Hell on Wheels', 'Infierno sobre ruedas', 2011], ['Kingdom', 'Kingdom', 2019], ['Spooks', 'Spooks', 2002], ['The Good Fight', 'La batalla ejemplar', 2017], ['86', '86', 2021], ['Somebody Somewhere', 'Alguien en algún lugar', 2022], ['The Wonder Years', 'Los años maravillosos', 1988], ['Narcos: México', 'Narcos: México', 2018], ['Dragon Ball Super: Doragon bôru cho', 'Dragon Ball Super', 2015], ['Made in Abyss', 'Made in Abyss', 2017], ['Tengen toppa gurren lagann', 'Tengen toppa gurren lagann', 2007], ['Harley Quinn', 'Harley Quinn', 2019], ['Rescue Me', 'Rescue Me', 2004], ['Oshi no Ko', 'Oshi no Ko', 2023], ['Extras', 'Extras', 2005], ['Life on Mars', 'Life on Mars', 2006], ['Farzi', 'Falso', 2023], ['Cranford', 'Cranford', 2007], ['Key and Peele', 'Key and Peele', 2012], ['Welcome to Wrexham', 'Bienvenido al Wrexham', 2022], ['Jung-jeung-eui-sang-sen-teo', 'Héroes de guardia', 2025], ['Winning Time: The Rise of the Lakers Dynasty', 'Lakers: Tiempo de ganar', 2022], ['DuckTales', 'PatoAventuras', 2017], ['Julia', 'Julia', 2022], ['Courage the Cowardly Dog', 'Coraje, el perro cobarde', 1999], ['Mary Tyler Moore', 'Mary Tyler Moore', 1970], ['The Avengers', 'Los vengadores', 1961], ["The Avengers: Earth's Mightiest Heroes", 'Los Vengadores: Los héroes más poderosos del planeta', 2010], ['The Daily Show', 'The Daily Show', 1996], ['Green Wing', 'Green Wing', 2004], ['Treme', 'Treme', 2010], ['The Mighty Boosh', 'The Mighty Boosh', 2003], ['Amphibia', 'Amphibia', 2019], ['Dragon Ball Kai: Doragon bôru kai', 'Dragon ball Z kai', 2009], ['Saiki Kusuo no Psi Nan', 'Saiki Kusuo no Psi Nan', 2016], ['Yeokdoyojeong Gim Bokju', 'Weightlifting Fairy Kim Bok-Joo', 2016]]


headers = {
    "Authorization": f"Bearer {TOKEN}"
}

excepciones = {("The Chosen", 2017): 85077, ("Mister Rogers' Neighborhood", 1968): 15, ("Gintama", 2005): 57041, ("El Chavo del Ocho", 1972): 47, ("Endeavour", 2012): 44264, ("The Venture Bros.", 2003): 2418, ("Mystery Science Theater 3000", 1988): 1952, ("Bosch", 2014): 60585, ("Common Side Effects", 2024): 228878, ("Babylon 5", 1993): 3137, ("Asur: Welcome to Your Dark Side", 2020): 308789, ("'Allo 'Allo!", 1982): 2211, ("The Kids in the Hall", 1988): 1551, ("The Adventures of Pete & Pete", 1992): 2824, ("The Mighty Boosh", 2003): 7166, ("Ore dake Reberu Appu na Ken", 2024): 127532, ("Sarabhai V/S Sarabhai", 2004): 4165, ("Binsenjo", 2021): 117376, ("Blackadder II", 1986): 7246, ("Blackadder the Third", 1987): 7246, ("Blackadder Goes Forth", 1989): 7246, ("Bleach: Sennen Kessen-hen", 2022): 30984, ("Twin Peaks", 2017): 1920, ("Sutîru Bôru Ran JoJo no Kimyô na Bôken", 2026): 45790, ("Dragon Ball", 1995): 12609, ("Dragon Ball Z", 1996): 12971}

omitir = {("Pew News", 2018), ("Content Cop", 2015), ("The Heroes", 2008)}

series = []
no_encontradas = []
ids_guardados = set()

for titulo_original, titulo_castellano, anio in lista:

    clave = (titulo_original, anio)
    id_serie = None

    if clave in omitir:
        no_encontradas.append((titulo_original, titulo_castellano, anio))
        continue

    if clave in excepciones:
        id_serie = excepciones[clave]

    else:
        titulos = [titulo_original]

        if titulo_castellano != titulo_original:
            titulos.append(titulo_castellano)

        for titulo in titulos:

            respuesta = requests.get(
                "https://api.themoviedb.org/3/search/tv",
                headers=headers,
                params={
                    "query": titulo,
                    "first_air_date_year": anio,
                    "language": "es-ES"
                },
                timeout=15
            )

            respuesta.raise_for_status()

            resultados = respuesta.json()["results"]

            coincidencias = []

            for resultado in resultados:
                if resultado.get("first_air_date", "")[:4] == str(anio):
                    coincidencias.append(resultado)

            if len(coincidencias)!=0:
                id_serie = coincidencias[0]["id"]
                break

    if id_serie is None:
        no_encontradas.append((titulo_original, titulo_castellano, anio))
        continue

    if id_serie in ids_guardados:
        continue

    respuesta2 = requests.get(
        f"https://api.themoviedb.org/3/tv/{id_serie}",
        headers=headers,
        params={
            "append_to_response": "credits,aggregate_credits",
            "language": "es-ES"
        },
        timeout=15
    )

    respuesta2.raise_for_status()

    detalles = respuesta2.json()

    duraciones = detalles.get("episode_run_time") or []

    if len(duraciones)!=0:
        duracion_media = sum(duraciones) / len(duraciones)
    else:
        duracion_media = None
    
    #Inicio código generado con IA
    creadores = []

    for persona in detalles.get("created_by", []):
        creadores.append(persona["name"])

    directores = []

    for persona in detalles.get("aggregate_credits", {}).get("crew", []):
        for trabajo in persona.get("jobs", []):
            if trabajo.get("job") == "Director":
                if persona["name"] not in directores:
                    directores.append(persona["name"])
                break

    actores = []

    for persona in detalles.get("aggregate_credits", {}).get("cast", [])[:10]:
        actores.append(persona["name"])
    #Final código generado con IA

    generos = []

    for genero in detalles["genres"]:
        generos.append(genero["name"])

    info = {
        "id": detalles["id"],
        "name": detalles["name"],
        "episode_run_time": duracion_media,
        "first_air_date": detalles["first_air_date"],
        "genres": generos,
        "number_of_episodes": detalles["number_of_episodes"],
        "number_of_seasons": detalles["number_of_seasons"],
        "origin_country": detalles["origin_country"],
        "vote_average": detalles["vote_average"],
        "creadores": creadores,
        "directores": directores,
        "actores": actores
    }

    series.append(info)
    ids_guardados.add(id_serie)

# Inicio código generado con IA
def guardar_json(series):
    with open("series_tmdb.json", "w", encoding="utf-8") as fichero:
        json.dump(series, fichero, ensure_ascii=False, indent=4)
# Final código generado con IA

guardar_json(series)

print("Series obtenidas:", len(series))
print("Series no encontradas:", len(no_encontradas))
