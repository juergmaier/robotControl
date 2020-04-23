# inmoovServoControl
inmoovServoControl stub for passing requests to the arduinos and publish updates of servos

Used libraries:
rpyc, simplejson, pyserial

Use rpyc to request actions.
Open a connection on a client: (see inmooveServoGui for an example)
inmoovServoControlRequest = rpyc.connect(config.INMOOV_SERVO_CONTROL_SERVER, config.INMOOV_SERVO_CONTROL_PORT, \
                                 config={"allow_all_attrs": True, "allow_pickle": True})

Exposed methods of inmoovServoControl:

exposed_startListening(self, clientIP, clientPort)
  a client can get servo updates by sending its IP and Port information
  
exposed_getServoDict(self)
  returns the json-ized servoDict

exposed_getServoDict(self)
  returns the json-ized min/max definitions for servo control
  
exposed_getServoCurrentList(self)
  list of current servo states

exposed_getArduinoData(self)
  list of Arduino connection states

exposed_requestServoPos(self, servoName, position, duration)
  move servo to given position within duration milliseconds
  
exposed_requestServoDegrees(self, servoName, degrees, duration)
  move servo to given degrees within duration milliseconds

exposed_getPosition(self, servoName)
  query basic servo data, current degrees, position and moving flag

legacy, for use with mrl gesture commands
exposed_getServoCurrent(self, servoName)
  returns position (0..180)

exposed_requestSetAutoDetach(self, servoName, milliseconds)
  change millis for auto detach after target reached, 0 = never detach

exposed_moveToRestDegrees(self, servoName)
  move servo to its rest degrees, leave servo name empty to rest all servos

exposed_requestServoStop(self, servoName)
  detach (stop) a servo

exposed_requestAllServosStop(self)
  detach (stop) all servos
  
exposed_requestSetPosition(self, servoName, newPosition)
  overwrite current servo position with new value

exposed_requestSetVerbose(self, servoName, newState)
  enable/disable detail log messages about servo moves

exposed_restAll(self)
  move all servos to their defined rest degrees

