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

