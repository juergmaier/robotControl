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


