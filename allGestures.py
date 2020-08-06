
import time
import config
import i01
import ear



isNeopixelActivated = False


def about():

	startGesture()

	setArmSpeed("right", 0.1, 0.1, 0.2, 0.2);
	setArmSpeed("left", 0.1, 0.1, 0.2, 0.2);
	setHeadSpeed(0.2,0.2)
	i01.moveArm("left", 64, 94, 10, 10);
	
	i01.mouth.speakBlocking(u"Ich bin der erste humanoide lebensgrosse roboter den man selber herstellen und bewegen kann")

	i01.moveHead(65,66)
	i01.moveArm("left", 64, 104, 10, 11);
	i01.moveArm("right", 44, 84, 10, 11);
	#i01.mouth.speakBlocking("my designer creator is Gael Langevin, a French sculptor")
	i01.mouth.speakBlocking(u"Mein Diseiner ist Gael Langevin aus Frankreich")
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


def ok():
  i01.moveHead(90,90,85,85,5)
  i01.moveArm("left",30,50,50,20) #brso
  i01.moveHand("left",0,180,180,180,180,25)
  sleep(5)
  relax()




# part of self repair video, look at left forarm
def checkforearms():
  setArmSpeed("right", 0.95,0.95,0.95,0.95) 
  i01.moveArm("right", 67, 90, 95, 10)  #brso
  i01.moveHead(20,40)
  sleep(10)

  setArmSpeed("left", 0.95,0.95,0.95,0.95) 
  i01.moveArm("left", 67, 90, 93, 10)  #brso
  setHeadSpeed(0.80, 0.80)
  i01.moveHead(20,135)
  sleep(10)

  i01.moveHead(20,40)
  sleep(7)

  rest()



def closelefthand():
  i01.moveHand("left",180,180,180,180,180)




def closerighthand():
  i01.moveHand("right",180,180,180,180,180)




def comehere():
    fullspeed()
    relax()
##look around
    setHeadSpeed(0.80, 0.80)
    setEyeSpeed(0.90, 0.90, 1.0)
    i01.moveHead(80,66,7,85,52)
    sleep(3)
    i01.moveHead(80,110,175,85,52)
    sleep(3)
##raise arm point finger
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 1.0, 0.85, 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 0.90, 1.0, 1.0, 1.0)
    setHeadSpeed(1.0, 0.90)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(80,86,85,85,52)
    i01.moveArm("left",5,94,30,10)
    i01.moveArm("right",7,74,92,10)
    i01.moveHand("left",180,180,180,180,180,90)
    i01.moveHand("right",180,2,175,160,165,180)
    i01.moveTorso(90,90,90)
    sleep(4.5)
##move finger
    setHandSpeed("left", 250, 250, 250, 250, 250, 250)
    setHandSpeed("right", 250, 250, 250, 250, 250, 250)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(1.0, 1.0)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(80,86)
    i01.moveArm("left",5,94,30,10)
    i01.moveArm("right",48,74,92,10)
    i01.moveHand("left",180,180,180,180,180,90)
    i01.moveHand("right",180,2,175,160,165,20)
    i01.moveTorso(90,90,90)
    sleep(2)
    setHeadSpeed(0.80, 0.80)
    i01.moveHead(80,80)
    i01.moveHand("right",180,164,175,160,165,20)
    sleep(1)
    i01.moveHead(80,80)
    i01.moveHand("right",180,2,175,160,165,20)
    sleep(1)
    i01.moveHead(118,80)
    i01.moveHand("right",180,164,175,160,165,20)
    sleep(1)
    i01.mouth.speak("come closer")
    i01.moveHead(60,80)
    i01.moveHand("right",180,2,175,160,165,20)
    sleep(1)
    i01.moveHead(118,80)
    i01.moveHand("right",180,164,175,160,165,20)
    sleep(1)
    i01.moveHead(60,80)
    i01.moveArm("right",90,65,10,25)
    sleep(3)
    fullspeed()
    rest()
    sleep(0.3)
    relax()
    sleep(3)
    fullspeed()


def cyclegesture1():
    welcome()
    sleep(1)
    relax()
    servos()


def cyclegesture2():
  ##for x in range(5):
    welcome()
    sleep(1)
    relax()
    sleep(2)
    fingerright()
    sleep(1)
    isitaball()
    sleep(2)
    removeleftarm()
    sleep(2)
    handdown()
    sleep(1)
    fullspeed()
    i01.giving()
    sleep(5)
    removeleftarm()
    sleep(4)
    takeball()
    sleep(1)
    surrender()
    sleep(6)
    isitaball()
    sleep(6)
    dropit()
    sleep(2)
    removeleftarm()
    sleep(5)
    relax()
    sleep()
    fullspeed()
    sleep(5)
    madeby()
    relax()
    sleep(5)
    i01.detach()


def cyclegesture3():
    rest()
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(0.9, 0.9)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(50,110)
    i01.moveArm("left",88,90,70,23)
    i01.moveArm("right",73,90,70,27)
    i01.moveHand("left",2,2,2,2,2,90)
    i01.moveHand("right",2,2,2,2,2,90)
    i01.moveTorso(90,90,90)
    sleep(2)
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(0.9, 0.8)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(50,70)
    i01.moveArm("left",88,90,75,28)
    i01.moveArm("right",80,90,76,21)
    i01.moveHand("left",180,180,180,180,180,90)
    i01.moveHand("right",180,180,180,180,180,90)
    i01.moveTorso(90,90,90)
    sleep(1)
    setHandSpeed("left", 0.95, 0.95, 0.95, 0.95, 0.95, 1.0)
    setHandSpeed("right", 0.95, 0.95, 0.95, 0.95, 0.95, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(0.9, 0.8)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(40,70)
    i01.moveArm("left",90,82,70,23)
    i01.moveArm("right",80,82,68,27)
    i01.moveHand("left",2,2,2,2,2,90)
    i01.moveHand("right",2,2,2,2,2,90)
    i01.moveTorso(90,90,90)
    sleep(2)
    i01.moveHead(50,100)
    i01.moveArm("left",88,90,70,28)
    i01.moveArm("right",75,90,76,21)
    i01.moveHand("left",180,180,180,180,180,10)
    i01.moveHand("right",180,180,180,180,180,170)
    i01.moveTorso(90,90,90)
    sleep(2)
    i01.moveHead(50,70)
    i01.moveArm("left",88,90,75,28)
    i01.moveArm("right",80,90,76,21)
    i01.moveHand("left",180,180,180,180,180,170)
    i01.moveHand("right",180,180,180,180,180,10)
    i01.moveTorso(90,90,90)
    sleep(3)
    setHandSpeed("left", 0.9, 0.9, 0.9, 0.9, 0.9, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(0.9, 0.9)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(79,160)
    i01.moveArm("left",5,84,32,80)
    i01.moveArm("right",87,82,123,74)
    i01.moveHand("left",0,0,0,0,0,25)
    i01.moveHand("right",0,0,0,0,0,113)
    i01.moveTorso(170,90,90)
    sleep(6)
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    setHeadSpeed(0.8, 0.8)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(79,100)
    i01.moveArm("left",18,84,55,71)
    i01.moveArm("right",65,82,118,15)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",81,66,82,60,105,113)
    i01.moveTorso(90,90,90)
    sleep(1)
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 0.9,  0.9,  0.9,  0.9)
    setArmSpeed("right",  0.9,  0.9,  0.9,  0.9)
    setHeadSpeed(0.8, 0.8)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(60,50)
    i01.moveArm("left",18,84,54,69)
    i01.moveArm("right",65,82,118,13)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",180,180,180,180,180,113)
    i01.moveTorso(40,90,90)
    sleep(2)
    i01.moveHead(79,100)
    i01.moveArm("left",33,84,136,80)
    i01.moveArm("right",34,82,160,13)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",180,180,180,180,180,113)
    i01.moveTorso(90,90,90)
    sleep(2)
    ##arm right up
    i01.moveHead(100,100)
    i01.moveArm("left",33,84,136,80)
    i01.moveArm("right",34,82,160,20)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",92,33,37,71,66,113)
    i01.moveTorso(90,90,90)
    sleep(3)
    i01.moveHead(110,120)
    i01.moveArm("left",33,140,136,80)
    i01.moveArm("right",34,82,170,30)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",92,33,37,71,66,113)
    i01.moveTorso(90,90,90)
    sleep(2)
    i01.moveHead(125,140)
    i01.moveArm("left",33,90,36,60)
    i01.moveArm("right",34,80,170,40)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",92,33,37,71,66,113)
    i01.moveTorso(30,90,90)
    sleep(2)
    ##arm left up
    i01.moveHead(120,130)
    i01.moveArm("left",33,90,36,60)
    i01.moveArm("right",34,65,160,40)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",92,33,37,71,66,113)
    i01.moveTorso(50,90,90)
    sleep(2)
    i01.moveHead(79,100)
    i01.moveArm("left",18,84,54,69)
    i01.moveArm("right",65,78,118,13)
    i01.moveHand("left",92,33,37,71,66,30)
    i01.moveHand("right",180,180,180,180,180,113)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(79,100)
    i01.moveArm("left",18,84,55,71)
    i01.moveArm("right",75,80,120,45)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",81,66,82,60,105,113)
    i01.moveTorso(90,90,90)
    sleep(1)
    setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 0.85)
    setHeadSpeed(0.9, 0.9)
    setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(79,160)
    i01.moveArm("left",24,84,32,74)
    i01.moveArm("right",87,82,123,74)
    i01.moveHand("left",0,0,0,0,0,25)
    i01.moveHand("right",0,0,0,0,0,113)
    i01.moveTorso(130,90,90)
    sleep(3)
    i01.moveHead(60,20)
    i01.moveArm("left",87,82,123,74)
    i01.moveArm("right",5,84,32,80)
    i01.moveHand("left",92,33,37,71,66,25)
    i01.moveHand("right",81,66,82,60,105,113)
    i01.moveTorso(30,90,90)
    sleep(6)
    setHeadSpeed(1.0,1.0)
    setArmSpeed("left",1.0,1.0,1.0,1.0)
    setArmSpeed("right",1.0,1.0,1.0,1.0)
    i01.moveHead(80,86)
    i01.moveArm("left",5,90,30,10)
    i01.moveArm("right",5,90,30,10)
    i01.moveTorso(90,90,90)
    sleep(2)
    i01.mouth.speakBlocking("wow, I feel good, I love this")
    sleep(2)
    rest()
    sleep(1)
    relax()


def datestring (display_format="%a, %d %b %Y %H:%M:%S", datetime_object=None):
  if datetime_object is None:
    datetime_object = datetime.utcnow()
  return datetime.strftime(datetime_object, display_format)

def daVinci():
  i01.startedGesture()
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, 22.0)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, 22.0)
  i01.setArmVelocity("left", 36, 36, 36, 36)
  i01.setArmVelocity("right", 36, 36, 36, 36)
  i01.setHeadVelocity(31.0, 31.0)
  i01.moveHead(80,90)
  i01.moveArm("left",0,118,29,74)
  i01.moveArm("right",0,118,29,74)
  i01.moveHand("left",50,40,30,20,10,47)
  i01.moveHand("right",50,40,30,20,10,137)
  sleep(5)
  i01.finishedGesture()



def delicategrab():
  setHandSpeed("left", 0.70, 0.60, 1.0, 1.0, 1.0, 1.0)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(1.0, 1.0)
  i01.moveHead(21,98)
  i01.moveArm("left",30,72,77,10)
  i01.moveArm("right",0,91,28,17)
  i01.moveHand("left",180,130,4,0,0,180)
  i01.moveHand("right",86,51,133,162,153,180)


def detach():
    i01.detach()



def DisplayPic(pic):
  r=0
  try:
    r=image.displayFullScreen(pic,1)
  except: 
    inmoovWebKit.getResponse("PICTUREPROBLEM")
    pass
  time.sleep(0.1)
  try:
    r=image.displayFullScreen(pic,1)
  except:
      pass

def dontworry():
  i01.startedGesture()
  i01.setHandVelocity("left", 50, 50, 50, 50, 50, 59)
  i01.setHandVelocity("right", 50, 50, 50, 50, 50, 59)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", 50, -1, -1, -1)
  i01.moveHead(116,80)
  i01.moveArm("left",85,93,42,16)
  i01.moveArm("right",87,93,37,18)
  i01.moveHand("left",124,82,65,81,41,143)
  i01.moveHand("right",59,53,89,61,36,21)
  i01.moveTorso(90,90,90)
  i01.mouth.speak("mmmmmmh, I sense much fear in you")
  sleep(2)
  i01.finishedGesture()
  relax()
    


def dropit():
  i01.setHandVelocity("left", 100, 100, 100, 100, 100, 100)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.75, 0.85, 0.95, 0.85)
  setArmSpeed("left", 0.75, 0.85, 1.0, 0.85)
  setHeadSpeed(0.75, 0.75)
  i01.moveHead(20,99)
  i01.moveArm("left",5,45,87,31)
  i01.moveArm("right",5,82,33,15)
  sleep(3)
  i01.moveHand("left",60,61,67,34,34,35)
  i01.moveHand("right",20,40,40,30,30,72)




def eatindianfood():
  fullspeed()
  i01.startedGesture()
  i01.setHeadVelocity(43.0, 36, 50, 50, -1)
  i01.moveHead(60,40,7,85,52)
  sleep(1)
  i01.moveHead(80,40,7,85,52)
  sleep(2)
  i01.setHeadVelocity(0.92, 36, 50, 50, -1)
  i01.moveHead(100,40,7,85,52)
  sleep(0.4)
  i01.moveArm("left",85,106,25,18)
  i01.moveArm("right",87,107,32,18)
  i01.moveHand("left",110,62,56,88,81,145)
  i01.moveHand("right",78,88,101,95,81,27)
  i01.moveTorso(90,90,90)
  i01.moveHead(80,40,7,85,52)
  i01.mouth.speakBlocking("yes, i want some paneer tikka")
  sleep(1)
  i01.moveHead(60,90,80,90,52)
  sleep(0.8)
  i01.finishedGesture()
  relax()


# python method to start gesture
def endGesture():
  i01.finishedGesture()
  ear.startListening()

def eyesdown():
    i01.head.eyeY.moveTo(180)



def eyesfront():
  i01.startedGesture()
  i01.head.eyeX.moveTo(90)
  i01.head.eyeY.moveTo(90)
  i01.finishedGesture()



def eyesleft():
  i01.startedGesture()
  i01.head.eyeX.moveTo(180)
  sleep(1)
  i01.finishedGesture()



def eyeslooking(data):
  for y in range(0, 5):
    if (data == "can i have your attention"):
      i01.mouth.speak("ok you have my attention")
      stopit()
    if (data == "inmoov"):
      stopit()
    x = (random.randint(1, 6))
    if x == 1:
      i01.head.eyeX.moveTo(80)
    if x == 2:
      i01.head.eyeY.moveTo(80)
    if x == 3:
      eyesdown()
    if x == 4:
      eyesupp()
    if x == 5:
      eyesleft()
    if x == 6:
      eyesright()
    sleep(0.5)
  eyesfront()



def eyesright():
  i01.startedGesture()
  i01.head.eyeX.moveTo(0)
  sleep(1)
  i01.finishedGesture()



def eyesup():
  i01.startedGesture()
  i01.head.eyeY.moveTo(0)
  sleep(1)
  i01.finishedGesture()


"""
def facerecognizer(): 
  #you need to train at least 2 FACES !   
  i01.cameraOn()
  fr=i01.vision.setActiveFilter("FaceRecognizer")
  fr.setMode(OpenCVFilterFaceRecognizer.Mode.TRAIN)
  fr.train()# it takes some time to train and be able to recognize face
  fr.setMode(OpenCVFilterFaceRecognizer.Mode.RECOGNIZE)
"""

def fighter():
  i01.startedGesture()
  i01.moveHead(160,87)
  i01.moveArm("left",31,75,152,10)
  i01.moveArm("right",3,94,33,16)
  i01.moveHand("left",161,151,133,127,107,83)
  i01.moveHand("right",99,130,152,154,145,180)
  i01.moveTorso(90,90,90)
  sleep(1)
  i01.finishedGesture()


def fingerleft():
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", -1, 43.0, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", 50, -1, -1, -1)
  i01.setHeadVelocity(-1, 50)
  i01.setTorsoVelocity(50.0, 13.0, -1)
  i01.moveHead(80,86)
  i01.moveArm("left",7,78,92,10)
  i01.moveArm("right",5,94,20,10)
  i01.moveHand("left",180,2,175,160,165,90)
  i01.moveHand("right",180,180,180,180,180,90)
  i01.moveTorso(120,110,90)




def fingerright():
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", -1, 43.0, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", 50, -1, -1, -1)
  i01.setHeadVelocity(-1, 50)
  i01.setTorsoVelocity(50.0, 13.0, -1)
  i01.moveHead(80,86)
  i01.moveArm("left",5,94,20,10)
  i01.moveArm("right",7,78,92,10)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,2,175,160,165,180)
  i01.moveTorso(60,70,90)



def finnishhello():
  i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(105,78)
  i01.moveArm("left",78,48,37,11)
  i01.moveArm("right",90,144,60,75)
  i01.moveHand("left",112,111,105,102,81,10)
  i01.moveHand("right",0,0,0,50,82,180)
  sleep(1)

  for w in range(0,3):
    i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
    i01.setHandVelocity("right", -1, -1, -1, -1, -1, 19)
    i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
    i01.setArmVelocity("right", 19, -1, -1, -1)
    i01.setHeadVelocity(22.0, 31.0)
    i01.moveHead(83,98)
    i01.moveArm("left",78,48,37,11)
    i01.moveArm("right",90,157,47,75)
    i01.moveHand("left",112,111,105,102,81,10)
    i01.moveHand("right",3,0,62,41,117,94)


    if w==1:
        i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
        i01.setHandVelocity("right", -1, -1, -1, -1, -1, 19)
        i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
        i01.setArmVelocity("right", 22.0, -1, -1, -1)
        i01.setHeadVelocity(22.0, 31.0)
        i01.moveHead(83,70)
        i01.mouth.speakBlocking("hei, nimeni on inmoov")
        i01.moveArm("left",78,48,37,11)
        i01.moveArm("right",57,145,50,68)
        i01.moveHand("left",100,90,85,80,71,15)
        i01.moveHand("right",3,0,31,12,26,45)
        sleep(1)
        i01.moveHead(83,98)
        i01.moveArm("left",78,48,37,11)
        i01.moveArm("right",90,157,47,75)
        i01.moveHand("left",112,111,105,102,81,10)
        i01.moveHand("right",3,0,62,41,117,94)
        sleep(1)
        i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, 43.0)
        i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, 43.0)
        i01.setArmVelocity("right", 31.0, 43.0, 59, 43.0)
        i01.setArmVelocity("left", 59, 22.0, 31.0, 31.0)
        i01.setHeadVelocity(31.0, 31.0)
        i01.moveHead(79,100)
        i01.moveArm("left",5,94,28,15)
        i01.moveArm("right",5,82,28,15)
        i01.moveHand("left",42,58,42,55,71,35)
        i01.moveHand("right",81,50,82,60,105,113)

def fistHips():
  i01.startedGesture()
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(-1, -1)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(138,80)
  i01.moveArm("left",79,42,23,41)
  i01.moveArm("right",71,40,14,39)
  i01.moveHand("left",180,180,180,180,180,47)
  i01.moveHand("right",99,130,152,154,145,180)
  i01.moveTorso(90,90,90)
  i01.finishedGesture()

def fisthips():
  i01.startedGesture()
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(138,80)
  i01.moveArm("left",79,45,23,41)
  i01.moveArm("right",71,40,14,39)
  i01.moveHand("left",180,180,180,180,180,47)
  i01.moveHand("right",99,130,152,154,145,180)
  i01.moveTorso(90,90,90)
  i01.finishedGesture()



def fullspeed():
  setHandSpeed("left", 250, 250, 250, 250, 250, 250)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(1.0, 1.0)
  setTorsoSpeed(1.0, 1.0, 1.0)



def gestureforlondon3():
  i01.startedGesture()
#welcome  
  i01.setHandVelocity("left", 19, 19, 19, 19, 19, 19)
  i01.setHandVelocity("right", 19, 36, 19, 19, 19, 19)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  i01.moveHead(0,90,90,50,65)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  sleep(5)
#welcome close hand
  i01.setHandVelocity("left", 59, 59, 59, 59, 59, -1)
  i01.setHandVelocity("right", 59, 59, 59, 59, 59, -1)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  i01.moveHead(0,40,25,40,65)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,180,180,180,180,90)
  sleep(3)
#put hands up  
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50.0, 50.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(50,120,90,90,65)
  i01.moveArm("left",88,103,70,23)
  i01.moveArm("right",73,97,70,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  i01.moveTorso(90,90,90)
  sleep(2)
#look hand right  
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50.0, 36.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(50,60,70,90,65)
  i01.moveArm("left",88,104,75,28)
  i01.moveArm("right",80,97,76,21)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,180,180,180,180,90)
  i01.moveTorso(90,90,90)
  sleep(1)
#look stay   
  i01.setHandVelocity("left", 59, 59, 59, 59, 59, -1)
  i01.setHandVelocity("right", 59, 59, 59, 59, 59, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50.0, 36.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(40,70,90,90,65)
  i01.moveArm("left",90,102,70,23)
  i01.moveArm("right",80,97,68,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  i01.moveTorso(90,90,90)
  sleep(2)
#look left side  turn both wrist 
  i01.moveHead(50,120,140,90,65)
  i01.moveArm("left",88,103,70,28)
  i01.moveArm("right",75,97,76,21)
  i01.moveHand("left",180,180,180,180,180,10)
  i01.moveHand("right",180,180,180,180,180,170)
  i01.moveTorso(90,90,90) 
  sleep(2)
#close hands and turn both wrist 
  i01.moveHead(50,50,60,90,65)
  i01.moveArm("left",88,103,75,28)
  i01.moveArm("right",80,97,76,21)
  i01.moveHand("left",180,180,180,180,180,170)
  i01.moveHand("right",180,180,180,180,180,10)
  i01.moveTorso(90,90,90)   
  sleep(3)
#dab left  
  i01.setHandVelocity("left", 50.0, 50.0, 50.0, 50.0, 50.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50.0, 50.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(79,160,120,90,65)
  i01.moveArm("left",5,84,32,78)
  i01.moveArm("right",87,82,123,74)
  i01.moveHand("left",0,0,0,0,0,25)
  i01.moveHand("right",0,0,0,0,0,113)
  i01.moveTorso(90,90,90)
  sleep(6)
#regroup right arm  
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(36.0, 36.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(79,100,120,90,65)
  i01.moveArm("left",18,90,55,71)
  i01.moveArm("right",65,82,118,15)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",81,66,82,60,105,113)
  i01.moveTorso(90,90,90)
  sleep(1)
#look right  
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", 50.0, 50.0, 50.0, 50.0)
  i01.setArmVelocity("right", 50.0, 50.0, 50.0, 50.0)
  i01.setHeadVelocity(36.0, 36.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(60,50,70,90,65)
  i01.moveArm("left",18,90,54,69)
  i01.moveArm("right",65,82,118,13)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",180,180,180,180,180,113)
  i01.moveTorso(90,90,90)
  sleep(2)
  i01.moveHead(79,100)
  i01.moveArm("left",33,90,136,78)
  i01.moveArm("right",34,82,160,13)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",180,180,180,180,180,113)
  i01.moveTorso(90,90,90)
  sleep(2)
#arm right up
  i01.moveHead(100,100)
  i01.moveArm("left",33,90,136,78)
  i01.moveArm("right",34,82,160,20)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",92,33,37,71,66,113)
  i01.moveTorso(90,90,90)
  sleep(3)
  i01.moveHead(110,120)
  i01.moveArm("left",33,140,136,78)
  i01.moveArm("right",34,82,170,30)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",92,33,37,71,66,113)
  i01.moveTorso(90,90,90)
  sleep(2)
  i01.moveHead(125,140)
  i01.moveArm("left",33,90,36,60)
  i01.moveArm("right",34,80,170,40)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",92,33,37,71,66,113)
  i01.moveTorso(90,90,90)
  sleep(2)
#arm left up
  i01.moveHead(120,130,120,30,65)
  i01.moveArm("left",33,90,36,60)
  i01.moveArm("right",34,65,160,40)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",92,33,37,71,66,113)
  i01.moveTorso(90,90,90)
  sleep(2)
  i01.moveHead(79,100,90,90,65)
  i01.moveArm("left",18,84,54,69)
  i01.moveArm("right",65,78,118,13)
  i01.moveHand("left",92,33,37,71,66,30)
  i01.moveHand("right",180,180,180,180,180,113)
  i01.moveTorso(90,90,90)
  sleep(1)
  i01.moveHead(79,100)
  i01.moveArm("left",18,90,55,71)
  i01.moveArm("right",75,80,120,45)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",81,66,82,60,105,113)
  i01.moveTorso(90,90,90)
  sleep(1)
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1, -1, -1, 43.0)
  i01.setHeadVelocity(50.0, 50.0)
  i01.setTorsoVelocity(-1, -1, -1)
  i01.moveHead(79,160)
  i01.moveArm("left",24,90,32,74)
  i01.moveArm("right",87,82,123,74)
  i01.moveHand("left",0,0,0,0,0,25)
  i01.moveHand("right",0,0,0,0,0,113)
  i01.moveTorso(90,90,90)
  sleep(3)
#dab right  
  i01.moveHead(60,20)
  i01.moveArm("left",87,90,123,74)
  i01.moveArm("right",5,84,32,78)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",81,66,82,60,105,113)
  i01.moveTorso(90,90,90)
  sleep(6)
#welcome  
  i01.setHandVelocity("left", 36, 36, 36, 36, 36, 36)
  i01.setHandVelocity("right", 36, 36, 36, 36, 36, 36)
  i01.setArmVelocity("left", 36, 36, 36, 36)
  i01.setArmVelocity("right", 36, 36, 36, 36)
  i01.setHeadVelocity(50, 50)
  i01.moveHead(0,90,90,50,65)
  i01.moveArm("left",15,105,30,25)
  i01.moveArm("right",25,124,30,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  sleep(5) 
  i01.finishedGesture()


def gestureforlondon4():
  if isNeopixelActivated:
    i01.setNeopixelAnimation("Color Wipe", 0, 20, 0, 1)
    sleep(2)
    i01.setNeopixelAnimation("Ironman", 0, 0, 255, 1)
  i01.startedGesture()
#welcome  
  i01.setHandVelocity("left", 19, 19, 19, 19, 19, 19)
  i01.setHandVelocity("right", 19, 36, 19, 19, 19, 19)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(0,90,90,50,65)
  i01.moveHead(0,90)
  i01.head.rollNeck.moveTo(90)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  sleep(5)
#welcome close hand
  i01.setHandVelocity("left", 59, 59, 59, 59, 59, -1)
  i01.setHandVelocity("right", 59, 59, 59, 59, 59, -1)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(0,40,25,40,65)
  i01.moveHead(0,40)
  i01.head.rollNeck.moveTo(50)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,180,180,180,180,90)
  sleep(3)
#welcome close hand 2
  i01.setHandVelocity("left", 59, 59, 59, 59, 59, -1)
  i01.setHandVelocity("right", 59, 59, 59, 59, 59, -1)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(0,40,25,40,65)
  i01.moveHead(0,120)
  i01.head.rollNeck.moveTo(120)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,180,180,180,180,90)
  sleep(3)
#welcome close hand3
  i01.setHandVelocity("left", 59, 59, 59, 59, 59, -1)
  i01.setHandVelocity("right", 59, 59, 59, 59, 59, -1)
  i01.setArmVelocity("left", 19, 19, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(0,40,25,40,65)
  i01.moveHead(0,90)
  i01.head.rollNeck.moveTo(90)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",180,180,180,180,180,90)
  i01.moveHand("right",180,180,180,180,180,90)
  sleep(3)  
#davinci  
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,10,42,50,65)
  i01.moveHead(46,10)
  i01.head.rollNeck.moveTo(50)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",61,49,14,38,15,64)
  i01.moveHand("right",0,24,54,50,82,180)
  i01.moveTorso(95,90,90)
  sleep(2)
#davinci turn wrist 1 
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,10,42,50,65)
  i01.moveHead(46,10)
  i01.head.rollNeck.moveTo(50)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",61,49,14,38,15,64)
  i01.moveHand("right",0,24,54,50,82,10)
  i01.moveTorso(95,90,90)
  sleep(1) 
#davinci turn wrist 2  
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,10,42,50,65)
  i01.moveHead(46,10)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",61,49,14,38,15,64)
  i01.moveHand("right",180,180,180,180,180,180)
  i01.moveTorso(95,90,90)
  sleep(2) 
#davinci turn wrist 3 
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,10,42,50,65)
  i01.moveHead(46,10)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",61,49,14,38,15,64)
  i01.moveHand("right",0,24,54,50,82,10)
  i01.moveTorso(95,90,90)
  sleep(1) 
#davinci  
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,10,42,50,65)
  i01.moveHead(46,10)
  i01.head.rollNeck.moveTo(90)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",61,49,14,38,15,64)
  i01.moveHand("right",0,24,54,50,82,180)
  i01.moveTorso(95,90,90)
  sleep(1)
#davinci turn head close hand 1   
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(-1, -1)
  #i01.moveHead(46,160,130,40,65)
  i01.moveHead(46,160)
  i01.head.rollNeck.moveTo(120)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",180,180,180,180,180,10)
  i01.moveHand("right",0,24,54,50,82,180)
  i01.moveTorso(95,90,90)
  sleep(2)
#davinci turn head close hand 2   
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  i01.moveHead(46,160)
  #i01.moveHead(46,160,130,40,65)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",0,0,0,0,0,180)
  i01.moveHand("right",0,24,54,50,82,180)
  i01.moveTorso(95,90,90)
  sleep(2)
#davinci turn head close hand 3   
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 50)
  #i01.moveHead(46,160,130,40,65)
  i01.moveHead(46,160)
  i01.moveArm("left",9,115,28,80)
  i01.moveArm("right",13,118,26,80)
  i01.moveHand("left",180,180,180,180,180,10)
  i01.moveHand("right",0,24,54,50,82,180)
  i01.moveTorso(95,90,90)
  sleep(2)         
#close hands and turn both wrist 
  #i01.moveHead(50,50,60,90,65)
  i01.moveHead(50,50)
  i01.head.rollNeck.moveTo(90)
  i01.moveArm("left",88,103,75,28)
  i01.moveArm("right",80,97,76,21)
  i01.moveHand("left",180,180,180,180,180,170)
  i01.moveHand("right",180,180,180,180,180,10)
  i01.moveTorso(90,90,90)   
  sleep(3)
#dab left  
  i01.setHandVelocity("left", 50.0, 50.0, 50.0, 50.0, 50.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50.0, 50.0)
  i01.setTorsoVelocity(31.0, 31.0, -1)
  #i01.moveHead(79,160,120,90,65)
  i01.moveHead(79,160)
  i01.moveArm("left",5,84,32,78)
  i01.moveArm("right",87,82,123,74)
  i01.moveHand("left",0,0,0,0,0,25)
  i01.moveHand("right",0,0,0,0,0,113)
  i01.moveTorso(170,120,90)
  sleep(6)
#arms up and centered  
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", 50.0, 50.0, 50.0, 50.0)
  i01.setArmVelocity("right", 50.0, 50.0, 50.0, 50.0)
  i01.setHeadVelocity(36.0, 36.0)
  i01.setTorsoVelocity(31.0, 31.0, -1)
  #i01.moveHead(60,50,70,90,65)
  i01.moveHead(60,50)
  i01.moveArm("left",75,90,120,10)
  i01.moveArm("right",75,90,120,10)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",180,180,180,180,180,113)
  i01.moveTorso(90,90,90) 
  sleep(3)
#dab right
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, -1)
  i01.setArmVelocity("left", 50.0, 50.0, 50.0, 50.0)
  i01.setArmVelocity("right", 50.0, 50.0, 50.0, 50.0)
  i01.setHeadVelocity(36.0, 36.0)
  i01.setTorsoVelocity(31.0, 31.0, -1)  
  i01.moveHead(60,20)
  i01.moveArm("left",87,90,123,74)
  i01.moveArm("right",5,84,32,80)
  i01.moveHand("left",92,33,37,71,66,25)
  i01.moveHand("right",81,66,82,60,105,113)
  i01.moveTorso(40,70,90)
  sleep(6)
#welcome  
  i01.setHandVelocity("left", 36, 36, 36, 36, 36, 36)
  i01.setHandVelocity("right", 36, 36, 36, 36, 36, 36)
  i01.setArmVelocity("left", 36, 36, 36, 36)
  i01.setArmVelocity("right", 36, 36, 36, 36)
  i01.setHeadVelocity(50, 50)
  i01.setTorsoVelocity(31.0, 31.0, -1)  
  #i01.moveHead(0,90,90,50,65)
  i01.moveHead(0,90)
  i01.moveArm("left",15,105,30,20)
  i01.moveArm("right",25,124,30,20)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  i01.moveTorso(90,90,90)
  sleep(5)
  i01.finishedGesture()


def getball():
  rest()
  i01.startedGesture()
  i01.setHandVelocity("right", 43.0, 31.0, 31.0, 31.0, 43.0, 31.0)
  i01.setArmVelocity("right", -1, -1, -1, 43.0)
  i01.setHeadVelocity(50.0, 50.0)
  i01.setTorsoVelocity(31.0, 13.0, -1)
  i01.moveHead(45,65)
  i01.moveArm("left",5,90,16,15)
  i01.moveArm("right",6,85,110,22)
  i01.moveHand("left",50,50,40,20,20,90)
  i01.moveHand("right",0,0,0,3,0,11)
  i01.moveTorso(101,100,90)
  sleep(2.5)
  i01.moveHand("right",180,140,140,3,0,11)
  sleep(1)
  i01.finishedGesture()



def givethebottle():
  i01.startedGesture()
  i01.setHandVelocity("left", 19, 19, 19, 19, 19, 31.0)
  i01.setHandVelocity("right", 19, 36, 19, 19, 19, 19)
  i01.setArmVelocity("left", 36, 36, 43.0, 36)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(22.0, 22.0)
  i01.moveHead(0,92)
  i01.moveHead(20,107,82,78,65)
  i01.moveArm("left",77,85,45,20)
  i01.moveArm("right",80,62,38,10)
  i01.moveHand("left",80,90,90,90,180,80)
  i01.moveHand("right",145,112,127,105,143,150)
  i01.moveTorso(90,82,90)
  sleep(1)
  i01.finishedGesture()



def givetheglass():
  i01.startedGesture()
  sleep(2)
  i01.setHandVelocity("left", 19, 19, 19, 19, 19, 19)
  i01.setHandVelocity("right", 19, 36, 19, 19, 19, 19)
  i01.setArmVelocity("left", 19, -1, 19, 19)
  i01.setArmVelocity("right", 19, 19, 19, 19)
  i01.setHeadVelocity(22.0, 22.0)
  i01.moveHead(84,79)
  i01.moveArm("left",77,75,45,17)
  i01.moveArm("right",21,80,77,10)
  i01.moveHand("left",109,138,180,164,180,60)
  i01.moveHand("right",102,86,105,105,143,133)
  i01.mouth.speakBlocking("Hello please take the glass")
  sleep(1)
  i01.finishedGesture()



def giving():
  fullspeed()
  i01.startedGesture()
  if (i01.isCameraOn()):
    #i01.moveHead(44,82)
    i01.moveArm("left",15,55,68,10)
    i01.moveArm("right",13,40,74,13)
    i01.moveHand("left",61,0,14,0,0,180)
    i01.moveHand("right",0,24,24,19,21,25)
    i01.moveTorso(90,90,90)
  else:
    i01.moveHead(44,82)
    i01.moveArm("left",15,55,68,10)
    i01.moveArm("right",13,40,74,13)
    i01.moveHand("left",61,0,14,0,0,180)
    i01.moveHand("right",0,24,24,19,21,25)
    i01.moveTorso(90,90,90)
  i01.finishedGesture()  


def grabthebottle():
  i01.startedGesture()
  i01.setHandVelocity("left", -1, 36, 36, 36, -1, 36)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(50, 36)
  i01.setTorsoVelocity(-1,36,-1)
  i01.moveHead(20,107)
  i01.moveArm("left",77,85,45,20)
  i01.moveArm("right",5,90,30,10)
  i01.moveHand("left",180,138,140,164,180,60)
  i01.moveHand("right",0,0,0,0,0,90)
  i01.moveTorso(90,84,90)
  sleep(1)
  i01.finishedGesture()



def grabtheglass():
  i01.startedGesture()
  i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, 19, 19, -1, -1, 36)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(22.0, 22.0)
  i01.setTorsoVelocity(-1,43.0,-1)
  i01.moveHead(20,68)
  i01.moveArm("left",77,85,45,15)
  i01.moveArm("right",48,91,72,20)
  i01.moveHand("left",180,138,140,164,180,50)
  i01.moveHand("right",140,112,127,105,143,140)
  i01.moveTorso(105,105,90)
  sleep(1)
  i01.finishedGesture()



def guesswhat():
  i01.mouth.speak("I'm not really a human man")
  i01.mouth.speak("but I use Old spice body wash and deodorant together")
  i01.mouth.speak("and now I'm really cool")

  




def handdown():
  i01.startedGesture()
  i01.setHandVelocity("left", 31.0, 31.0, 31.0, 31.0, 31.0, 31.0)
  i01.setHandVelocity("right", 26.00, 26.00, 26.00, 26.00, 26.00, -1)
  i01.setArmVelocity("right", 43.0, 22.0, 22.0, 22.0)
  i01.moveHead(18,75)
  i01.moveArm("left",66,52,59,23)
  i01.moveArm("right",59,60,50,16)
  i01.moveHand("left",140,148,140,10,10,0)
  i01.moveHand("right",54,95,66,0,0,11)
  sleep(2)
  i01.finishedGesture()



def handsclose():
  i01.moveHand("left",180,180,180,180,180)
  i01.moveHand("right",180,180,180,180,180)



def handsopen():
  i01.moveHand("left",0,0,0,0,0)
  i01.moveHand("right",0,0,0,0,0)



def happy():
  i01.startedGesture()
  for w in range(0,3):
    sleep(1)
    i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
    i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
    i01.setArmVelocity("right", 43.0, 43.0, 43.0, -1)
    i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
    i01.setHeadVelocity(22.0, 22.0)
    i01.moveHead(84,88)
    i01.moveArm("left",5,82,36,10)
    i01.moveArm("right",74,112,61,29)
    i01.moveHand("left",0,88,135,94,96,90)
    i01.moveHand("right",81,79,118,47,0,90)
    sleep(1)
    if w==1:
        i01.mouth.speakBlocking("happy birthday grog")
        i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
        i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
        i01.setArmVelocity("right", 43.0, 43.0, 43.0, -1)
        i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
        i01.setHeadVelocity(22.0, 22.0)
        i01.moveHead(42,76)
        i01.moveArm("left",5,90,30,10)
        i01.moveArm("right",74,70,61,10)
        i01.moveHand("left",0,0,0,0,0,90)
        i01.moveHand("right",81,79,118,47,0,90)
        sleep(5)
  i01.startedGesture()    
        


def headdown():
  i01.head.neck.moveTo(0)



def headfront():
  i01.head.neck.moveTo(90)
  i01.head.rothead.moveTo(90)



def headleft():
  i01.head.rothead.moveTo(180)



def headright():
  i01.head.rothead.moveTo(0)



def headupp():
  i01.head.neck.moveTo(180)



def hello():
  i01.startedGesture()
  i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(105,78)
  i01.moveArm("left",78,48,37,11)
  i01.moveArm("right",90,144,60,75)
  i01.moveHand("left",112,111,105,102,81,10)
  i01.moveHand("right",0,0,0,50,82,180)
  sleep(1)
  i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, 19)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", 19, -1, -1, -1)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(83,98)
  i01.moveArm("left",78,48,37,11)
  i01.moveArm("right",90,157,47,75)
  i01.moveHand("left",112,111,105,102,81,10)
  i01.moveHand("right",3,0,62,41,117,94)
  sleep(1)
  i01.setHandVelocity("left", 19, 19, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, 19)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("right", 22.0, -1, -1, -1)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(83,70)
  i01.moveArm("left",78,48,37,11)
  i01.moveArm("right",57,145,50,68)
  i01.moveHand("left",100,90,85,80,71,15)
  i01.moveHand("right",3,0,31,12,26,45)
  sleep(1)
  i01.moveHead(83,98)
  i01.moveArm("left",78,48,37,11)
  i01.moveArm("right",90,157,47,75)
  i01.moveHand("left",112,111,105,102,81,10)
  i01.moveHand("right",3,0,62,41,117,94)
  sleep(1)
  i01.setHandVelocity("left", 43.0, 43.0, 43.0, 43.0, 43.0, 43.0)
  i01.setHandVelocity("right", 43.0, 43.0, 43.0, 43.0, 43.0, 43.0)
  i01.setArmVelocity("right", 31.0, 43.0, 59, 43.0)
  i01.setArmVelocity("left", 59, 22.0, 31.0, 31.0)
  i01.setHeadVelocity(31.0, 31.0)
  i01.moveHead(79,100)
  i01.moveArm("left",5,94,28,15)
  i01.moveArm("right",5,82,28,15)
  i01.moveHand("left",42,58,42,55,71,35)
  i01.moveHand("right",81,50,82,60,105,113)
  sleep(2)
  i01.finishedGesture()
  relax()



def hi():
    i01.startedGesture()
    i01.halfSpeed()
    relax()
    i01.startedGesture()
    i01.moveHead(80,86,10)
    leftHandX = (random.randint(1, 2))
    if leftHandX==1:i01.moveHand("left",180,0,0,180,180,0)
    else:i01.moveHand("left",0,180,180,180,180,0)
    i01.moveArm("left",180,140,40,180)
    i01.moveTorso(90,70,90)
    sleep(2)
    i01.moveHead(80,86,180)
    sleep(5)
    relax()
    sleep(2)
    i01.finishedGesture()

def howdoyoudo():
  global helvar
  if helvar < 1:
    helvar += 1
  elif helvar == 1:
    i01.moveArm("left",43,88,22,10)
    i01.moveArm("right",20,90,30,10)
    i01.moveHand("left",0,0,0,0,0,119)
    i01.moveHand("right",0,0,0,0,0,119)
    sleep(2)
    relax()
    helvar += 1
  elif helvar == 2:
    i01.moveArm("left",30,83,22,10)
    i01.moveArm("right",40,85,30,10)
    i01.moveHand("left",130,180,180,180,180,119)
    i01.moveHand("right",130,180,180,180,180,119)
    sleep(2)
    relax()
    helvar += 1
  elif helvar >= 3:
    helvar=4
    unhappy()
    sleep(4)
    relax()    
  i01.chatBot.setPredicate("parameterHowDoYouDo",str(helvar))

def howmanyfingersdoihave():
  i01.startedGesture()
  fullspeed()
  i01.moveHead(49,74)
  i01.moveArm("left",75,83,79,24)
  i01.moveArm("right",65,82,71,24)
  i01.moveHand("left",74,140,150,157,168,92)
  i01.moveHand("right",89,80,98,120,114,0)
  sleep(2)
  i01.moveHand("right",0,80,98,120,114,0)
  i01.mouth.speakBlocking("10")

  sleep(.1)
  i01.moveHand("right",0,0,98,120,114,0)
  i01.mouth.speakBlocking("9")

  sleep(.1)
  i01.moveHand("right",0,0,0,120,114,0)
  i01.mouth.speakBlocking("8")

  sleep(.1)
  i01.moveHand("right",0,0,0,0,114,0)
  i01.mouth.speakBlocking("7")

  sleep(.1)
  i01.moveHand("right",0,0,0,0,0,0)
  i01.mouth.speakBlocking("6")

  sleep(.5)
  i01.setHeadVelocity(.70,.70)
  i01.moveHead(40,105)
  i01.moveArm("left",75,83,79,24)
  i01.moveArm("right",65,82,71,24)
  i01.moveHand("left",0,0,0,0,0,180)
  i01.moveHand("right",0,0,0,0,0,0)
  sleep(0.1)
  if Language=="fr":
    i01.mouth.speakBlocking("et 5 font 11")
  else:
    i01.mouth.speakBlocking("and five makes eleven")

  sleep(0.7)
  i01.setHeadVelocity(26.0,26.0)
  i01.moveHead(40,50)
  sleep(0.5)
  i01.setHeadVelocity(26.0,26.0)
  i01.moveHead(49,105)
  sleep(0.7)
  i01.setHeadVelocity(26.0,36.0)
  i01.moveHead(40,50)
  sleep(0.7)
  i01.setHeadVelocity(26.0,36.0)
  i01.moveHead(49,105)
  sleep(0.7)
  i01.setHeadVelocity(26.0,26.0)
  i01.moveHead(90,85)
  sleep(0.7)
  i01.mouth.speakBlocking("11")
  i01.moveArm("left",70,75,70,20)
  i01.moveArm("right",60,75,65,20)
  sleep(1)
  if Language=="fr":
    i01.mouth.speakBlocking("oupse, cela semble incorect, je vais reessayer")
  else:
    i01.mouth.speakBlocking("that doesn't seem right, I think I better try that again")


  i01.moveHead(40,105)
  i01.moveArm("left",75,83,79,24)
  i01.moveArm("right",65,82,71,24)
  i01.moveHand("left",140,168,168,168,158,90)
  i01.moveHand("right",87,138,109,168,158,25)
  sleep(2)

  i01.moveHand("left",10,140,168,168,158,90)
  i01.mouth.speakBlocking("1")
  sleep(.1)


  i01.moveHand("left",10,10,168,168,158,90)
  i01.mouth.speakBlocking("2")
  sleep(.1)

  i01.moveHand("left",10,10,10,168,158,90)
  i01.mouth.speakBlocking("3")
  sleep(.1)
  i01.moveHand("left",10,10,10,10,158,90)

  i01.mouth.speakBlocking("4")
  sleep(.1)
  i01.moveHand("left",10,10,10,10,10,90)

  i01.mouth.speakBlocking("5")
  sleep(.1)
  i01.setHeadVelocity(22.0,22.0)
  i01.moveHead(53,65)
  i01.moveArm("right",48,80,78,11)
  i01.setHandVelocity("left", -1, -1, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.moveHand("left",10,10,10,10,10,90)
  i01.moveHand("right",10,10,10,10,10,25)
  sleep(1)
  if Language=="fr":
    i01.mouth.speakBlocking("et 5 font 10")
  else:
    i01.mouth.speakBlocking("and five makes ten")
  sleep(.5)
  if Language=="fr":
    i01.mouth.speakBlocking("c'est beaucoup mieux")
  else:
    i01.mouth.speakBlocking("it is better")
  i01.moveHead(95,85)
  i01.moveArm("left",75,83,79,24)
  i01.moveArm("right",40,70,70,10)
  sleep(0.5)
  if Language=="fr":
    i01.mouth.speakBlocking("inemouve a 10 doigts")
  else:
    i01.mouth.speakBlocking("inmoov has 10 fingers")
  sleep(0.5)
  i01.moveHead(90,90)
  i01.setHandVelocity("left", 36.0, 36.0, 36.0, 36.0, 36.0, 36.0)
  i01.setHandVelocity("right", 36.0, 36.0, 36.0, 36.0, 36.0, 36.0)
  i01.moveHand("left",140,140,140,140,140,60)
  i01.moveHand("right",140,140,140,140,140,60)
  sleep(-1)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setArmVelocity("left", -1.0, -1.0, -1.0, -1.0)
  i01.moveArm("left",5,90,30,11)
  i01.moveArm("right",5,90,30,11)
  sleep(0.5)
  i01.finishedGesture()
  relax()



def isitaball():
  setHandSpeed("left", 1.0, 1.0, 1.0, 0.8, 0.8, 0.90)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 1.0, 0.95, 0.95, 0.85)
  setArmSpeed("left", 0.75, 0.85, 0.90, 0.85)
  setHeadSpeed(0.65, 0.75)
  i01.moveHead(70,82)
  fullspeed()
  i01.moveArm("left",70,59,95,15)
  i01.moveArm("right",12,74,33,15)
  i01.moveHand("left",170,150,180,180,180,164)
  i01.moveHand("right",105,81,78,57,62,105)




# python function for keeping hand leveled
# called from the clock every x ms (see main script for interval)
def keepHandLeveled(time):
  global keepLeveled
  global bendServo
  global wristServo 
  global bno
  if not keepLeveled:
    print("keepLeveled")
    event = bno.getOrientationEuler()
    print("w,x,y,z,yaw,roll,pitch,temp,time")
    print(event.w, event.x, event.y, event.z, event.yaw, event.roll, event.pitch, event.temperature, event.timestamp)
    print("---")
  
  
    


def madeby():
    relax()
    sleep(1)
    i01.moveHead(80,86)
    i01.moveArm("left",5,90,30,10)
    i01.moveArm("right",5,90,30,10)
    i01.moveHand("left",45,40,30,25,35,90)
    i01.moveHand("right",55,2,50,48,30,90)
    i01.moveTorso(90,90,90)
    sleep(3)
    #i01.mouth.speakBlocking("hello")
    i01.mouth.speakBlocking("hallo")
    i01.moveHead(80,98)
    i01.moveArm("left",5,90,30,10)
    i01.moveArm("right",5,90,30,10)
    i01.moveHand("left",45,40,30,25,35,90)
    i01.moveHand("right",55,2,50,48,30,90)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(90,89)
    i01.moveArm("left",42,104,30,10)
    i01.moveArm("right",33,116,30,10)
    i01.moveHand("left",45,40,30,25,35,120)
    i01.moveHand("right",55,2,50,48,30,40)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(80,98)
    i01.moveArm("left",5,99,30,16)
    i01.moveArm("right",5,94,30,16)
    i01.moveHand("left",120,116,110,115,98,73)
    i01.moveHand("right",114,146,125,113,117,109)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("my name is inmoov")
    i01.mouth.speakBlocking("ich heisse Marvin, ich bin ein Roboter der InMoov Klasse")
    i01.moveHead(68,90)
    i01.moveArm("left",5,99,30,16)
    i01.moveArm("right",85,102,38,16)
    i01.moveHand("left",120,116,110,115,98,73)
    i01.moveHand("right",114,146,161,132,168,19)
    i01.moveTorso(90,90,90)
    sleep(0.5)
    ##setHandSpeed("left", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    ##setHandSpeed("right", 0.85, 0.85, 0.85, 0.85, 0.85, 1.0)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
    ##setHeadSpeed(1.0, 0.90)
    ##setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(87,94)
    i01.moveArm("left",5,99,36,16)
    i01.moveArm("right",81,105,42,16)
    i01.moveHand("left",120,116,110,115,98,50)
    i01.moveHand("right",114,118,131,132,168,19)
    i01.moveTorso(90,90,90)
    sleep(1)
    #i01.mouth.speakBlocking("I am created by gael langevin")
    i01.mouth.speakBlocking("Mein Erfinder ist Gael Langevin")
    setHandSpeed("left", 0.90, 0.90, 0.90, 0.90, 0.90, 0.95)
    setHandSpeed("right", 0.90, 0.90, 0.90, 0.90, 0.90, 0.95)
    setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
    setArmSpeed("right", 0.90, 1.0, 1.0, 1.0)
    ##setHeadSpeed(1.0, 0.90)
    ##setTorsoSpeed(1.0, 1.0, 1.0)
    i01.moveHead(105,94)
    i01.moveArm("left",5,99,36,16)
    i01.moveArm("right",81,105,42,16)
    i01.moveHand("left",120,116,110,115,98,50)
    i01.moveHand("right",114,118,131,132,168,19)
    i01.moveTorso(90,90,90)
    sleep(0.2)
    i01.moveHead(80,86)
    i01.moveArm("left",5,96,25,10)
    i01.moveArm("right",5,94,26,10)
    i01.moveHand("left",110,62,56,88,81,18)
    i01.moveHand("right",78,88,101,95,81,137)
    i01.moveTorso(90,90,90)
    sleep(0.2)
    i01.moveHead(75,97)
    i01.moveArm("left",85,106,25,18)
    i01.moveArm("right",87,107,32,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",78,88,101,95,81,27)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("who is a french sculptor, designer")
    i01.mouth.speakBlocking("ein Designer aus Frankreich")
    sleep(0.5)
    i01.moveHead(80,86)
    i01.moveArm("left",5,96,25,10)
    i01.moveArm("right",5,94,26,10)
    i01.moveHand("left",110,62,56,88,81,18)
    i01.moveHand("right",78,88,101,95,81,137)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(75,97)
    i01.moveArm("left",6,91,22,14)
    i01.moveArm("right",87,107,32,18)
    i01.moveHand("left",110,62,56,88,81,0)
    i01.moveHand("right",78,88,101,95,81,27)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("my software is being developped by myrobtlab dot org")
    i01.mouth.speakBlocking("Die Steuerung erfolgt mit der Software meirobotlaeb")
    sleep(1)
    i01.moveHead(20,69)
    i01.moveArm("left",6,91,22,14)
    i01.moveArm("right",87,107,32,21)
    i01.moveHand("left",110,62,56,88,81,0)
    i01.moveHand("right",78,88,101,95,81,27)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("I am totally build with 3 D printed parts")
    i01.mouth.speakBlocking("Ich bin aus etwa 200 Teilen zusammengebaut")
    i01.moveHead(75,97)
    i01.moveArm("left",85,106,25,18)
    i01.moveArm("right",87,107,32,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",78,88,101,95,81,27)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(33,110)
    i01.moveArm("left",85,104,25,18)
    i01.moveArm("right",87,41,47,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",111,75,117,125,111,143)
    i01.moveTorso(90,90,90)
    sleep(1)
    i01.moveHead(62,102)
    i01.moveArm("left",85,104,25,18)
    i01.moveArm("right",87,41,47,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",111,75,117,125,111,143)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("which means all my parts")
    i01.mouth.speakBlocking("Alle meine Teile")
    i01.moveHead(79,88)
    i01.moveArm("left",85,104,25,18)
    i01.moveArm("right",87,59,46,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",59,75,117,125,111,113)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("are made on a home 3 D printer")
    i01.mouth.speakBlocking("sind mit einem 3 d Drucker ausgedruckt worden")
    sleep(1)
    i01.moveHead(40,84)
    i01.moveArm("left",85,72,38,18)
    i01.moveArm("right",87,64,47,18)
    i01.moveHand("left",124,97,66,120,130,35)
    i01.moveHand("right",59,75,117,125,111,113)
    i01.moveTorso(90,90,90)
    #i01.mouth.speakBlocking("each parts are design to fit 12 centimeter cube build area")
    i01.mouth.speakBlocking("Jedes Teil hat maximal die Groesse von 12 mal 12 mal 12 centimeter")
    sleep(1)
    i01.moveHead(97,80)
    i01.moveArm("left",85,79,39,14)
    i01.moveArm("right",87,76,42,12)
    i01.moveHand("left",124,97,66,120,130,35)
    i01.moveHand("right",59,75,117,125,111,113)
    i01.moveTorso(90,90,90)
    sleep(0.5)
    i01.moveHead(75,97)
    i01.moveArm("left",85,106,25,18)
    i01.moveArm("right",87,107,32,18)
    i01.moveHand("left",110,62,56,88,81,145)
    i01.moveHand("right",78,88,101,95,81,27)
    i01.moveTorso(90,90,90)
    sleep(1)
    #i01.mouth.speakBlocking("so anyone can reproduce me")
    i01.mouth.speakBlocking("somit kann ich mit fast jedem 3 d drucker erzeugt werden")
    fullspeed()
    i01.moveHead(80,98)
    i01.moveArm("left",5,90,30,10)
    i01.moveArm("right",5,90,30,10)
    i01.moveHand("left",45,40,30,25,35,90)
    i01.moveHand("right",55,2,50,48,30,90)
    i01.moveTorso(90,90,90)
    sleep(1)
    #i01.mouth.speakBlocking("cool, don't you think")
    i01.mouth.speakBlocking("tolle sache, nicht wahr?")
    sleep(1)
    #i01.mouth.speakBlocking("thank you for listening")
    i01.mouth.speakBlocking("Danke fuer ihre Aufmerksamkeit")
    i01.moveHead(116,80)
    i01.moveArm("left",85,93,42,16)
    i01.moveArm("right",87,93,37,18)
    i01.moveHand("left",124,82,65,81,41,143)
    i01.moveHand("right",59,53,89,61,36,21)
    i01.moveTorso(90,90,90)
    sleep(0.2)
    relax()







handServos = ['Hand.thumb',
              'Hand.index',
              'Hand.majeure',
              'Hand.ringFinger',
              'Hand.pinky',
              'Hand.wrist']
handMoveDuration = {
    'leftHand.thumb' : {'default': 500, 'current': 500},
    'leftHand.index' : {'default': 500, 'current': 500},
    'leftHand.majeure' : {'default': 500, 'current': 500},
    'leftHand.ringFinger' : {'default': 500, 'current': 500},
    'leftHand.pinky' : {'default': 500, 'current': 500},
    'leftHand.wrist' : {'default': 500, 'current': 500},
    'rightHand.thumb' : {'default': 500, 'current': 500},
    'rightHand.index' : {'default': 500, 'current': 500},
    'rightHand.majeure' : {'default': 500, 'current': 500},
    'rightHand.ringFinger' : {'default': 500, 'current': 500},
    'rightHand.pinky' : {'default': 500, 'current': 500},
    'rightHand.wrist' : {'default': 500, 'current': 500}
}

armServos = ['Arm.bicep',
             'Arm.rotate',
             'Arm.shoulder',
             'Arm.omoplate']
armMoveDuration = {
    'leftArm.bicep' : {'default': 800, 'current': 800},
    'rightArm.bicep' : {'default': 800, 'current': 800},
    'leftArm.rotate' : {'default': 800, 'current': 800},
    'rightArm.rotate' : {'default': 800, 'current': 800},
    'leftArm.shoulder' : {'default': 800, 'current': 800},
    'rightArm.shoulder' : {'default': 800, 'current': 800},
    'leftArm.omoplate' : {'default': 800, 'current': 800},
    'rightArm.omoplate' : {'default': 800, 'current': 800} }


headServos = ['head.rothead',
              'head.neck']
headMoveDuration =  {'head.rothead' : {'default': 800, 'current': 800},
                     'head.neck': {'default': 800, 'current': 800}}

eyeServos = ['head.eyeX',
             'head.eyeY']
eyeMoveDuration =  {'head.eyeX' : {'default': 800, 'current': 800},
                    'head.eyeY': {'default': 800, 'current': 800}}

torsservoStatics = ['torso.topStom',
               'torso.midStom'
               'torso.lowStom']
torsoMoveDuration =  {'torso.topStom' : {'default': 800, 'current': 800},
                      'torso.midStom' : {'default': 800, 'current': 800},
                      'torso.lowStom' : {'default': 800, 'current': 800}}


gestureDir = 'c:/projekte/inmoov/robotControl/marvinGestures'   # change this to marvinGestures once all gestures are verified


def createAllGesturesModule():

    with open('allGestures.py','w') as wfd:

        wfd.writelines("from mrlGestures import *\n")
        wfd.writelines("import i01\n")
        wfd.writelines("import ear\n")
        wfd.writelines("\n")
        wfd.writelines("isNeopixelActivated = False\n")
        wfd.writelines("\n")

        for item in os.listdir(gestureDir):
            file = gestureDir + "/" + item
            config.log(f"adding file to allGestures: {item}")
            with open(file,'r') as fd:
                shutil.copyfileobj(fd, wfd)
                wfd.writelines("\n")
                wfd.writelines("\n")

    importlib.reload(allGestures)



def runSelectGesture(gestureName):
    gestureName()


def setHandSpeed(side, thumbSpeed, indexSpeed, majeureSpeed, ringFingerSpeed, pinkySpeed, wristSpeed):
    global handMoveDuration
    handMoveDuration[side + 'Hand.thumb']['current'] = handMoveDuration[side + 'Hand.thumb']['default'] / float(thumbSpeed)
    handMoveDuration[side + 'Hand.index']['current'] = handMoveDuration[side + 'Hand.index']['default'] / float(indexSpeed)
    handMoveDuration[side + 'Hand.majeure']['current'] = handMoveDuration[side + 'Hand.majeure']['default'] / float(majeureSpeed)
    handMoveDuration[side + 'Hand.ringFinger']['current'] = handMoveDuration[side + 'Hand.ringFinger']['default'] / float(ringFingerSpeed)
    handMoveDuration[side + 'Hand.pinky']['current'] = handMoveDuration[side + 'Hand.pinky']['default'] / float(pinkySpeed)
    handMoveDuration[side + 'Hand.wrist']['current'] = handMoveDuration[side + 'Hand.wrist']['default'] / float(wristSpeed)


def setArmSpeed(side, bicepSpeed, shoulderSpeed, rotateSpeed, omoplateSpeed):
    global armMoveDuration
    config.log(f"setArmSpeed {side}, {bicepSpeed}, {shoulderSpeed}, {rotateSpeed}, {omoplateSpeed}")
    armMoveDuration[side + 'Arm.bicep']['current'] = armMoveDuration[side + 'Arm.bicep']['default'] / float(bicepSpeed)
    armMoveDuration[side + 'Arm.rotate']['current'] = armMoveDuration[side + 'Arm.rotate']['default'] / float(rotateSpeed)
    armMoveDuration[side + 'Arm.shoulder']['current'] = armMoveDuration[side + 'Arm.shoulder']['default'] / float(shoulderSpeed)
    armMoveDuration[side + 'Arm.omoplate']['current'] = armMoveDuration[side + 'Arm.omoplate']['default'] / float(omoplateSpeed)


def setHeadSpeed(rotHeadSpeed, neckSpeed):
    global headMoveDuration
    headMoveDuration['head.rothead']['current'] = headMoveDuration['head.rothead']['default'] / float(rotHeadSpeed)
    headMoveDuration['head.neck']['current'] = headMoveDuration['head.neck']['default'] / float(neckSpeed)


def setTorsoSpeed(topStomSpeed, midStomSpeed, lowStomSpeed=800):
    global torsoMoveDuration
    torsoMoveDuration['torso.topStom']['current'] = torsoMoveDuration['torso.topStom']['default'] / float(topStomSpeed)
    torsoMoveDuration['torso.midStom']['current'] = torsoMoveDuration['torso.midStom']['default'] / float(midStomSpeed)

def setEyeSpeed(eyeXSpeed, eyeYSpeed):
    global eyeMoveDuration
    eyeMoveDuration['head.eyeX']['current'] = torsoMoveDuration['head.eyeX']['default'] / float(eyeXSpeed)
    eyeMoveDuration['head.eyeY']['current'] = torsoMoveDuration['head.eyeY']['default'] / float(eyeXSpeed)


def sleep(seconds=0):
    time.sleep(seconds)

def rest():
    i01.rest()

def relax():
    i01.rest()


def openlefthand():
  i01.moveHand("left",0,0,0,0,0)




def openrighthand():
  i01.moveHand("right",0,0,0,0,0)



def perfect():
  i01.startedGesture()
  i01.setHandVelocity("left", 36, 36, -1, -1, -1, -1)
  i01.setHandVelocity("right", -1, -1, -1, -1, -1, -1)
  i01.setArmVelocity("left", 59, 59, 59, -1)
  i01.setArmVelocity("right", -1.0, -1.0, -1.0, -1.0)
  i01.setHeadVelocity(22.0, 31.0)
  i01.moveHead(88,79)
  i01.moveArm("left",89,75,93,11)
  i01.moveArm("right",0,91,28,17)
  i01.moveHand("left",130,160,83,40,0,34)
  i01.moveHand("right",86,51,133,162,153,180)
  sleep(1)
  i01.mouth.speak("it is perfect")
  sleep(1)
  i01.finishedGesture()
  #i01.mouth.speak(u"Это идеально")
  



def removeleftarm():
  i01.setHandVelocity("left", 100, 100, 100, 100, 100, 100)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.75, 0.85, 0.95, 0.85)
  setArmSpeed("left", 0.95, 0.65, 0.75, 0.75)
  setHeadSpeed(0.75, 0.75)
  i01.moveHead(20,100)
  i01.moveArm("left",71,94,41,31)
  i01.moveArm("right",5,82,28,15)
  i01.moveHand("left",60,43,45,34,34,35)
  i01.moveHand("right",20,40,40,30,30,72)


def servos():

  startGesture()

  i01.leftArm.omoplate.enableAutoDisable(0)
  i01.rightArm.omoplate.enableAutoDisable(0)
  i01.head.neck.enableAutoDisable(0)

  ear.pauseListening()
  sleep(2)
  i01.setHandVelocity("left", 250, 250, 250, 250, 250, 250)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(79,100)
  i01.moveArm("left",5,119,28,15)
  i01.moveArm("right",5,111,28,15)
  i01.moveHand("left",42,58,87,55,71,35)
  i01.moveHand("right",81,20,82,60,105,113)
  i01.mouth.speakBlocking(u"Ich habe fuenf und zwanzig servo motoren in meinem koerper und ein paar weitere in meinem waegelchen")
  i01.setHandVelocity("left", 100, 100, 100, 100, 100, 100)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(124,90)
  i01.moveArm("left",89,94,91,35)
  i01.moveArm("right",20,67,31,22)
  i01.moveHand("left",106,41,161,147,138,90)
  i01.moveHand("right",0,0,0,54,91,90)
  i01.mouth.speakBlocking(u"es gibt einen Motor fuer die Lippenbewegung")
  sleep(1)
  i01.setHandVelocity("left", 100, 100, 250, 100, 100, 100)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(105,76);
  i01.moveArm("left",89,106,103,35);
  i01.moveArm("right",35,67,31,22);
  i01.moveHand("left",106,0,0,147,138,80);
  i01.moveHand("right",0,0,0,54,91,90);
  i01.mouth.speakBlocking(u"zwei kleine Motoren fuer die Augen")
  sleep(0.2)
  i01.moveHead(90,90,30,90,90);
  sleep(0.2)
  i01.moveHead(90,90,150,90,90);
  sleep(0.2)
  i01.moveHead(90,90,90,30,90);
  sleep(0.2)
  i01.moveHead(90,90,90,30,90);
  sleep(0.2)
  i01.moveHead(90,90,90,100,90);
  sleep(0.2)
  i01.moveHead(90,90,90,90,90);

  i01.mouth.speakBlocking(u"und zwei weitere fuer meine Kopfbewegung")
  sleep(0.5)
  i01.setHandVelocity("left", 100, 150, 150, 150, 150, 100)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(90,40);
  i01.moveArm("left",89,106,103,35);
  i01.moveArm("right",35,67,31,20);
  i01.moveHand("left",106,140,140,140,140,7);
  i01.moveHand("right",0,0,0,54,91,90);
  i01.mouth.speakBlocking(u"damit kann ich mich umschauen")
  sleep(0.5)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(105,125);

  setArmSpeed("left", 0.9, 0.9, 0.9, 0.9)
  i01.moveArm("left",60,100,85,30);
  i01.mouth.speakBlocking(u"und sehen wer hier ist")
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(40,80);
  sleep(0.5)
  i01.moveHead(40,67);

  setArmSpeed("right", 0.5, 0.6, 0.5, 0.6);
  i01.moveArm("left",87,41,64,11)
  i01.moveArm("right",5,95,40,11)
  i01.moveHand("left",98,150,160,160,160,104)
  i01.moveHand("right",0,0,50,54,91,90);
  i01.mouth.speakBlocking(u"in jeder Schulter gibt es 3 grosse motoren")

  sleep(2)
  i01.setHandVelocity("left", 90, 150, 90, 90, 90, 90)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.8, 0.8)
  i01.moveHead(43,69)
  i01.moveArm("left",87,41,64,11)
  i01.moveArm("right",5,95,40,42)
  i01.moveHand("left",42,0,100,80,113,35)
  i01.moveHand("left",42,10,160,160,160,35)
  i01.moveHand("right",81,20,82,60,105,113)
  i01.mouth.speakBlocking(u"hier die erste Bewegung")
  sleep(1)
  i01.moveHead(37,60);
  i01.setHandVelocity("left", 250, 250, 150, 150, 250, 90)
  setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
  i01.moveArm("right",5,95,67,42)
  i01.moveHand("left",42,10,10,160,160,30)
  i01.mouth.speakBlocking(u"dann die zweite")
  sleep(1)
  i01.moveHead(43,69);
  setArmSpeed("right", 1.0, 1.0, 1.0, 1.0)
  i01.moveArm("right",5,134,67,42)
  i01.moveHand("left",42,10,10,10,160,35)
  i01.mouth.speakBlocking(u"und jetzt die dritte")
  sleep(1)
  setArmSpeed("right", 0.8, 0.8, 0.8, 0.8)
  i01.moveArm("right",20,90,45,16)
  i01.mouth.speakBlocking(u"sie sind der menschlichen Schulter nachgeahmt")
  sleep(1)
  i01.setHandVelocity("left", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 1.0, 1.0, 1.0, 1.0);
  i01.moveHead(43,72)
  i01.moveArm("left",90,44,66,11)
  i01.moveArm("right",90,100,67,26)
  i01.moveHand("left",42,80,100,80,113,35)
  i01.moveHand("right",81,0,82,60,105,69)
  i01.mouth.speakBlocking(u"und ich habe einen weiteren Motor auf jeder Seite fuer die Ellbogen")
  i01.setHandVelocity("left", 100, 100, 100, 100, 100, 100)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0)
  setHeadSpeed(0.8, 0.8)
  i01.moveHead(45,62)
  i01.moveArm("left",72,44,90,11)
  i01.moveArm("right",90,95,68,15)
  i01.moveHand("left",42,0,100,80,113,90)
  i01.moveHand("right",81,0,82,60,105,0)
  i01.mouth.speakBlocking(u"des weiteren kann ich meine Hand drehen")
  i01.moveHead(40,60)
  i01.setHandVelocity("left", 250, 250, 250, 250, 250, 250)
  i01.setHandVelocity("right", 150, 150, 150, 150, 150, 250)
  i01.moveArm("left",72,44,90,9)
  i01.moveArm("right",90,95,68,15)
  i01.moveHand("left",42,0,100,80,113,150)
  i01.moveHand("right", 10, 140,82,60,105,10)
  i01.mouth.speakBlocking(u"und jeden Finger der Hand oeffnen und schliessen.")
  sleep(0.5)
  i01.moveHand("left", 150,   0, 100,  80, 113, 150)
  i01.moveHand("right", 10, 140,  82,  60, 105,  10)
  i01.mouth.speakBlocking(u"die Finger Motoren sind in meine Unterarme eingebaut")
  i01.setHandVelocity("left", 90, 90, 90, 90, 90, 90)
  i01.setHandVelocity("right", 250, 250, 250, 250, 250, 250)
  i01.moveHand("left", 42, 150, 100,  80, 113, 150)
  sleep(0.2)
  i01.moveHand("left",  42,   0,  20,  80, 113, 150)
  i01.moveHand("right",180, 140,  82,  60, 105,  10)
  sleep(0.2)
  i01.mouth.speakBlocking(u"und jeder Finger wird ueber zwei Angelschnuere vor und zurueck bewegt.")
  i01.moveHand("left",  42,   0, 100,  80, 113, 150)
  i01.moveHand("right", 10,  20,  82,  60, 105,  10)
  sleep(0.2)
  i01.moveHand("left",  42,   0, 100, 170, 113, 150)
  i01.moveHand("right", 10, 140,  30,  60, 105,  10)
  sleep(0.2)
  i01.moveHand("left",  42,   0, 100,  80,  20, 150)
  i01.moveHand("right", 10, 140,  82, 170, 105,  10)

  sleep(1)
  i01.moveHand("left",10,20,30,40,60,150);
  i01.moveHand("right",110,137,120,100,105,130);
  setHeadSpeed(1.0,1.0)
  setArmSpeed("right", 1.0,1.0, 1.0, 1.0);
  setArmSpeed("left", 1.0, 1.0, 1.0, 1.0);
  i01.mouth.speakBlocking(u"es steckt also viel Arbeit in meinem Koerper.")
  rest()
  sleep(2)
  ear.resumeListening()

  endGesture()


# python method to start gesture
def startGesture():
  i01.startedGesture()
  ear.stopListening()

def surrender(text=''):

  if text != '':
    mouth.speak(text)
  setHandSpeed("left", 250, 250, 250, 250, 250, 250)
  setHandSpeed("right", 250, 250, 250, 250, 250, 250)
  setArmSpeed("right", 0.75, 0.85, 0.95, 0.85)
  setArmSpeed("left", 0.75, 0.85, 0.95, 0.85)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(90,90)
  i01.moveArm("left",90,139,15,79)
  i01.moveArm("right",90,145,37,79)
  i01.moveHand("left",50,28,30,10,10,76)
  i01.moveHand("right",10,10,10,10,10,139)
  sleep(7)
  rest()
  sleep(2)



def takeball():
  rest()
  setHandSpeed("right", 0.85, 0.75, 0.75, 0.75, 0.85, 0.75)
  setArmSpeed("right", 0.85, 0.85, 0.85, 0.85)
  setHeadSpeed(0.9, 0.9)
  setTorsoSpeed(0.75, 0.55, 1.0)
  i01.moveHead(30,70)
  i01.moveArm("left",5,84,16,15)
  i01.moveArm("right",6,73,76,16)
  i01.moveHand("left",50,50,40,20,20,90)
  i01.moveHand("right",180,140,140,3,0,11)
  i01.moveTorso(120,100,90)



def welcome():
  sleep(1)
  setHandSpeed("left", 0.60, 0.60, 0.60, 0.60, 0.60, 0.60)
  setHandSpeed("right", 0.60, 0.80, 0.60, 0.60, 0.60, 0.60)
  setArmSpeed("left", 0.60, 0.60, 0.60, 0.60)
  setArmSpeed("right", 0.60, 0.60, 0.60, 0.60)
  setHeadSpeed(0.65, 0.65)
  i01.moveHead(80,90)
  i01.moveArm("left",26,105,30,25)
  i01.moveArm("right",37,124,30,27)
  i01.moveHand("left",2,2,2,2,2,90)
  i01.moveHand("right",2,2,2,2,2,90)
  sleep(1)
  i01.mouth.speakBlocking("Welcome to the inmoov nation")
  sleep(1)




