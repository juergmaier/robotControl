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

