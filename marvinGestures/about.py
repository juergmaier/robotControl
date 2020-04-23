def about():

	startGesture()

	setArmSpeed("right", 0.1, 0.1, 0.2, 0.2);
	setArmSpeed("left", 0.1, 0.1, 0.2, 0.2);
	setHeadSpeed(0.2,0.2)
	i01.moveArm("right", 64, 94, 10, 10);
	
	i01.mouth.speakBlocking(u"Ich bin der erste humanoide lebensgrosse roboter den man selber herstellen und bewegen kann")
	i01.moveHead(65,66)
	i01.moveArm("left", 64, 104, 10, 11);
	i01.moveArm("right", 44, 84, 10, 11);
	#i01.mouth.speakBlocking("my designer creator is Gael Langevin, a French sculptor")
	i01.mouth.speakBlocking(u"Mein Designer ist Gael Langevin aus Frankreich")
	i01.moveHead(75,86)
	i01.moveArm("left", 54, 104, 10, 11);
	i01.moveArm("right", 64, 84, 10, 20);
	#i01.mouth.speakBlocking("who has released my files  to the opensource three D world.")
	i01.mouth.speakBlocking("Er hat die 3 d elemente im internet frei verfuegbar gemacht und Anleitungen zum Zusammenbau erstellt.")
	i01.moveHead(65,96)
	i01.moveArm("left", 44, 94, 10, 20);
	i01.moveArm("right", 54, 94, 20, 11);
	#i01.mouth.speakBlocking("Jurg has downloaded these files and built me up from the many parts that I have.")
	i01.mouth.speakBlocking("Juerg hat diese Dateien herunter geladen und die beinahe zweihundert Teile auf seinem Multec 3 d Drucker ausgedruckt.")
	
	i01.moveHead(75,76)
	i01.moveArm("left", 64, 94, 20, 11);
	i01.moveArm("right", 34, 94, 10, 11);
	i01.mouth.speakBlocking("nach circa fuenf hundert Stunden druckzeit, vielen Kilos Plastik, fuenf und zwanzig hobby servos, viel Schweiss und Blut bin ich zur Welt gekommen.")
	i01.moveHead(65,86)
	i01.moveArm("left", 24, 94, 10, 11);
	i01.moveArm("right", 24, 94, 10, 11);  
	#i01.mouth.speakBlocking("so if You have a three D printer, some building skills and extra money, then you can build your own version of me") # mabe add in " alot of money"
	i01.mouth.speakBlocking("wenn sie also einen 3 d drucker haben oder beschaffen moechten, etwas Geschick mit Computer, Elektronik, Faeden und Schrauben haben und auch noch etwas Geld, koennen sie ihre eigene Kopie von mir erstellen")
	i01.moveHead(85,86)
	i01.moveArm("left", 5, 94, 20, 30);
	i01.moveArm("right", 24, 124, 10, 20);
	#i01.mouth.speakBlocking("and if enough people build me, some day my kind could take over the world") 
	i01.mouth.speakBlocking("und wenn genug Leute eine Kopie von mir erstellen, kann ich vielleicht auch die Weltherrschaft uebernehmen")
	
	i01.moveHead(75,96)
	i01.moveArm("left", 24, 104, 10, 11);
	i01.moveArm("right", 5, 94, 20, 30);
	#i01.mouth.speakBlocking("I'm just kidding. i need some legs to get around, and i have to over come my  pyro-phobia, a fear of fire")
	i01.mouth.speakBlocking("Das war natuerlich nur ein Spass, muss meine Angst vor Feuer noch ueberwinden")

	i01.moveHead(75,96)
	i01.moveArm("left", 5, 94, 10, 11)
	i01.moveArm("right", 4, 94, 10, 11);
	#i01.mouth.speakBlocking("so, until then. i will be humankind's humble servant")
	i01.mouth.speakBlocking("und somit, bis es soweit ist, bin ich nur ein Unterhalter und Zeit-Verbrater")
	
	i01.rest()
	setArmSpeed("right", 1, 1, 1, 1);
	setArmSpeed("left", 1, 1, 1, 1);
	setHeadSpeed(1,1)
	sleep(2)
	#ear.resumeListening()
        #i01.disable()

	endGesture()
