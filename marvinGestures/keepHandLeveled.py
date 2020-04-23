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
  
  
    
