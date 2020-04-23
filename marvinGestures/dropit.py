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


