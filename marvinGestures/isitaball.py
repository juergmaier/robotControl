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


