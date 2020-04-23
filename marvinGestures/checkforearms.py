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

