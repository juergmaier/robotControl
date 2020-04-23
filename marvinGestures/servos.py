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
