import sys
from random import randint

# hier wurden richtige Dinge getan..

class BacktrackingDurchLabyrinth():
	"""
	Klasse, mit welcher ein Spielfeld erstellt werden kann.
	Im Konstruktur werden die Dimensionen des Spielfeldes sowie die Anzahl der Hindernisse 
	Ã¼bergeben, um eine geeignete Instanz zu erzeugen.
	"""

	def __init__(self, breite, hoehe, hindernisse):
		MIN_BREITE = 10
		MAX_BREITE = 100
		MIN_HOEHE =  10
		MAX_HOEHE =  100
		MIN_HINDERNISSE =  10
		MAX_HINDERNISSE =  300

		# Fange Parameter ausserhalb des gÃ¼ltigen Bereichs ab und beende ProgrammausfÃ¼hrung mit Fehlermeldung
		if breite < MIN_BREITE or breite > MAX_BREITE:
			print("Breite liegt ausserhalb des gÃ¼ltigen Bereichs! Min: " , MIN_BREITE , " Max: " , MAX_BREITE);
			sys.exit(-1)
		elif hoehe < MIN_HOEHE or hoehe > MAX_HOEHE:
			print("HÃ¶he liegt ausserhalb des gÃ¼ltigen Bereichs! Min: " , MIN_HOEHE , " Max: " , MAX_HOEHE);
			sys.exit(-1)
		elif hindernisse < MIN_HINDERNISSE or hindernisse > MAX_HINDERNISSE:
			print("Anzahl Hindernisse liegt ausserhalb des gÃ¼ltigen Bereichs! Min: " , MIN_HINDERNISSE , " Max: " , MAX_HINDERNISSE);
			sys.exit(-1)
		
		
		self.breite = breite
		self.hoehe = hoehe
		self.hindernisse = hindernisse

		# Spielfeld in der Art eines zweidimensionalen Arrays. Hier bestehend aus aus zwei verschachtelten Listen, 
		# die jeweils ein Leerzeichen drucken. Die Listen werden mittels einer List Comprehension erzeugt.
		self.spielfeld = [ [' ' for x in range(self.breite)] for y in range(self.hoehe)]
		
		# Hier wird protokolliert, welche Wege man bereits abgegangen ist...
		self.bereits_besucht = [ ['('+str(x)+','+str(y)+')' for x in range(self.breite)] for y in range(self.hoehe)]


	def baue_spielfeld_auf(self):
		# Oberer Spielfeldrand aufbauen:
		for counter in range(0,self.breite):
			self.spielfeld[0][counter] = '#'

		
		# Seitliche Begrenzungen und Ziel aufbauen:
		for outer_counter in range(1,self.hoehe):
			for inner_counter in range(0,self.breite):
				# Linke und Rechte Begrenzung aufbauen:
				if inner_counter == 0 or inner_counter == self.breite-1:
					self.spielfeld[outer_counter][inner_counter] = '#'
					
				# Ziel platzieren:
				if outer_counter == self.hoehe-2 and inner_counter == self.breite-2:
					self.spielfeld[outer_counter][inner_counter] = 'O'

		# Unterer Spielfeldrand aufbauen:
		for counter in range(0, self.breite):
			self.spielfeld[self.hoehe-1][counter] = '#'



	def zeige_spielfeld_an(self):
		ANZAHL_LEERZEILEN = 50
		# ZunÃ¤chst Bildschirm leeren:
		for counter in range(1,ANZAHL_LEERZEILEN):
			print('\n')

		# Spielfeld anzeigen:
		for outer_counter in range(0, self.hoehe):
			for inner_counter in range(0, self.breite):
				print(self.spielfeld[outer_counter][inner_counter], end=" ")
				if inner_counter == self.breite-1:
					print('\n')
	

	#Hinternisse auf Spielfeld verteilen und Startfeld freirÃ¤umen:
	def verteile_hindernisse(self):
		for counter in range(0, self.hindernisse):
			#Die Hinternisse werden pseudo-zufÃ¤llig mittels der Funktion 'randint' aus dem zu Beginn importieren Modul
			#'random' importiert
			breite_ran = randint(1,self.breite-2)
			hoehe_ran = randint(1,self.hoehe-2)

			
			#Sicherstellen, dass Hindernisse nicht auf Zielfeld paltziert werden.
			if breite_ran != self.breite-2 or hoehe_ran != self.hoehe-2:
				self.spielfeld[hoehe_ran][breite_ran] = '*'

		#Element oben rechts im Koordinatensystem (1,1) frei machen -> dort startet Spielfigur
		self.spielfeld[1][1] = ' '


	#Rekursive Loesungsmethode starten:
	def schritt(self, x, y, x_alt, y_alt):
		input('Enter')

		#Abbruchbedingung fÃ¼r Rekursion, falls Spielfeld mit Ziel gefunden wurde:
		if self.spielfeld[x][y] == 'O':
			self.spielfeld[x][y] = 'P'
			self.spielfeld[x_alt][y_alt] = ' '
			
			self.zeige_spielfeld_an()

			print("Ziel erfolgreich mittels Backtracking gefunden!\n")
			#Daraufhin verlassen des Python-Programms:
			sys.exit()

		#falls man ansonsten auf ein freies Spielfeld stÃ¶ÃŸt, dieses als besucht markieren und die Spielfigur dahin verschieben,
		#die vorherige Platzierung der Spielfigur lÃ¶schen.
		elif self.spielfeld[x][y] == ' ':
			self.bereits_besucht[x][y] = '1'
			self.spielfeld[x][y] = 'P'
			self.spielfeld[x_alt][y_alt] = ' '
			
			self.zeige_spielfeld_an()
			
			#Falls man nach rechts ziehen kann, dort kein Hindernis existiert und man nicht dorther kam bzw. diesen
			#Ort bereits besucht hat -> gehe nach rechts
			if y+1 < self.breite-1 and self.spielfeld[x][y+1] != '*' and y_alt != y+1 and self.bereits_besucht[x][y+1] != '1' and self.schritt(x,y+1,x,y):
				return 1

			#Analog zu oben gehen nach rechts-unten
			elif y+1 < self.breite-1 and x+1 < self.hoehe-1 and self.spielfeld[x+1][y+1] != '*' and x_alt != x+1 and y_alt != y+1 and self.bereits_besucht[x+1][y+1] != '1' and self.schritt(x+1,y+1,x,y): 
				return 1

			#Analog zu oben gehen nach rechts-oben
			elif x-1 > 0 and y+1 < self.breite-1 and self.spielfeld[x-1][y+1] != '*' and x_alt != x-1 and y_alt != y+1 and self.bereits_besucht[x-1][y+1] != '1' and self.schritt(x-1, y+1, x,y):
				return 1
			
			#Analog zu oben gehen nach unten
			elif x+1 < self.hoehe-1 and self.spielfeld[x+1][y] != '*' and x_alt != x+1 and self.bereits_besucht[x+1][y] != '1' and self.schritt(x+1,y,x,y):
				return 1
			
			#Analog zu oben gehen nach links unten
			elif x+1 < self.hoehe-1 and y-1 > 0 and self.spielfeld[x+1][y-1] != '*' and x_alt != x+1 and y_alt != y-1 and self.bereits_besucht[x+1][y-1] != '1' and self.schritt(x+1,y-1,x,y):
				return 1
			
			#Analog zu oben gehen nach oben
			elif x-1 > 0 and self.spielfeld[x-1][y] != '*' and x_alt != x-1 and self.bereits_besucht[x-1][y] != '1' and self.schritt(x-1, y, x,y):
				return 1
			#Analog zu oben gehe nach links
			elif y-1 > 0 and self.spielfeld[x][y-1] != '*' and y_alt != y-1 and self.bereits_besucht[x][y-1] != '1' and self.schritt(x,y-1,x,y):
				return 1
			#Analog zu oben gehe nach links oben
			elif x-1 > 0  and y-1 > 0 and self.spielfeld[x-1][y-1] != '*' and x_alt != x-1 and y_alt != y-1 and self.bereits_besucht[x-1][y-1] != '1' and self.schritt(x-1, y-1, x,y):
				return 1
			
				

		self.spielfeld[x][y]	= ' '
		return 0


# Testen: Instanziieren der Klasse und prÃ¼fen der einzelnen Methoden:
meinLabyrinth = Backtracking_Durch_Labyrinth(50,15, 200)

meinLabyrinth.baue_spielfeld_auf()
meinLabyrinth.zeige_spielfeld_an()
meinLabyrinth.verteile_hindernisse()
meinLabyrinth.zeige_spielfeld_an()

meinLabyrinth.schritt(1,1,1,1)


# Es handelt sich hierbei um sauberen Code, da:
# Eine sinnvolle Benamung von Variablen gewählt wurde, so dass mittels der Namen die essentielle Bedeutung hervorkommt, aber die Länger der
# Variablen sinnvoll begrenzt ist. Zudem wurde weitestgehend auf den Einsatz von Magic Numbers verzichtet, stattdessen wurde mit symbolischen
# Konstanten gearbeitet. Einige wenige Werte, etwa die Randindizes von Arrays wurden so beibehalten, da sie zum Grundwissen für eine Python-Programmierer
# gehören. Es wurden bei bedingten Anweisungen nicht mit Negationen gearbeitet. Zudem wurde auf einer Abstraktionsebene gearbeitet, die Aufrufe erfolgen
# über die Methoden, innerhalb dieser wurde auf Aufrufe verzichtet und stattdessen Verarbeitungsschritte vorgenommen. 
# Zudem wurde die Möglichkeit von fehlerhafter Parametrisierung der Instanzvariablen durch Constraints verunmöglicht. Für einen solchen Fall wird die
# Programmausführung mit einem sinnvollen Text beendet. Es werden zudem keine NULL-Werte zurückgegeben.
# Schließlich bestätigte ein Test mit SonarQube, dass das Programm vernünftig geschrieben ist. 
