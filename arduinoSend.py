
import time
import config


def sendArduinoCommand(arduinoIndex, msg):
    if msg[-1] != "\n":
        msg += "\n"
    conn = config.arduinoConn[arduinoIndex]
    if conn is not None:
        #config.log(f"send msg to arduino {arduinoIndex}, {msg}")
        conn.write(bytes(msg, 'ascii'))
        conn.flush()
    else:
        config.log(f"no connection with arduino {arduinoIndex}")


def requestArduinoReady(arduino):

    msg = f"i,{arduino}\n"
    sendArduinoCommand(arduino, msg)
    config.log(f"request ready message from arduino {arduino}")


def servoAssign(servoName, lastPos):

    servoStatic = config.servoStaticDict[servoName]
    servoType = config.servoTypeDict[servoStatic.servoType]
    servoDerived = config.servoDerivedDict[servoName]

    # send servo definitions to the arduino's
    # both servo and servoType have an inverted flag. for our servo inversion is given if either of them
    # are set, double inversion or no inversion means normal operation of the servo
    invertedFlag = (servoStatic.inverted != servoType.typeInverted)
    inverted = 1 if invertedFlag else 0
    msg = f"0,{servoName},{servoStatic.pin},{servoStatic.minPos},{servoStatic.maxPos},{servoStatic.autoDetach:.1f},{inverted},{lastPos},{servoStatic.powerPin}\n"

    sendArduinoCommand(servoStatic.arduino, msg)

    config.log(f"assign servo: {servoName:<20}, \
pin: {servoStatic.pin:2}, minPos: {servoStatic.minPos:3}, maxPos:{servoStatic.maxPos:3}, \
restDeg: {servoStatic.restDeg:3}, autoDetach: {servoStatic.autoDetach:4.0f}, inverted: {inverted}, lastPos: {lastPos:3}, powerPin: {servoStatic.powerPin}")


def requestServoPosition(servoName, position, duration, filterSequence=True):
    """
    move servo in <duration> seconds from current position to <position>
    filter fast passed in requests
    """
    # command 1,<arduino>,<servo>,<position>,<duration>
    # e.g. servo=eyeX, position=50, duration=2500: 2,3,50,2500
    servoStatic = config.servoStaticDict[servoName]
    servoDerived = config.servoDerivedDict[servoName]
    servoCurrent = config.servoCurrentDict[servoName]

    # filter out jaw moves from log as they are very frequent
    if servoName != "head.jaw":
        config.log(f"arduino send {servoName}, arduino {servoStatic.arduino}, position: {position:.0f}, duration: {duration:.0f}", publish=False)

    # if new position requests come in heigh sequence avoid responding to each one
    # when filterSequence is active
    if filterSequence and (time.time() - servoCurrent.timeOfLastMoveRequest) < 0.2:
        config.log(f"move request ignored, time diff last request: {time.time() - servoCurrent.timeOfLastMoveRequest} s")
        return
    #else:
        #config.log(f"time since last move request: {time.time() - servoCurrent.timeOfLastMoveRequest}")

    servoCurrent.timeOfLastMoveRequest = time.time()

    if not servoStatic.enabled:
        config.log(f"servoPos {position} requested but servo is disabled in ServoDict.json")
        return

    # verify duration
    #config.log(f"position: {position}, scurrpos: {config.servoCurrent[servoName].position}")
    deltaPos = abs(config.servoCurrentDict[servoName].position - position)
    minDuration = servoDerived.msPerPos * deltaPos

    # for filtered moves increase move duration based on servos properties
    if duration < minDuration and filterSequence:
        config.log(f"{servoName}: duration increased, deltaPos: {deltaPos}, msPerPos: {servoDerived.msPerPos}, from: {duration:.0f} to: {minDuration:.1f}")
        duration = minDuration

    if config.simulateServoMoves:
        config.log(f"simulated move only")

    msg = f"1,{servoStatic.pin:02.0f},{position:03.0f},{duration:04.0f},{1 if config.simulateServoMoves else 0},\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def requestServoDegrees(servoName, degrees, duration):
    servoStatic = config.servoStaticDict[servoName]
    position = config.evalPosFromDeg(servoName, degrees)
    requestServoPosition(servoName, position, duration)


def requestServoStop(servoName):
    servoStatic = config.servoStaticDict[servoName]
    msg = f"2,{servoStatic.pin}\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def requestAllServosStop():
    config.log(f"all servos stop requested")
    msg = f"3\n"
    for i in range(config.numArduinos):
        if config.arduinoConn[i] is not None:
            sendArduinoCommand(i, msg)


def requestServoStatus(servoName):
    servoStatic = config.servoStaticDict[servoName]
    msg = f"4,{servoStatic.pin}\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def setAutoDetach(servoName, milliseconds):
    servoStatic = config.servoStaticDict[servoName]
    msg = f"5,{servoStatic.pin},{milliseconds}\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def setPosition(servoName, newPos):
    servoStatic = config.servoStaticDict[servoName]
    #servoControl.setPowerPin([servoStatic.powerPin])
    msg = f"6,{servoStatic.pin},{newPos}\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def setVerbose(servoName, state):
    servoStatic = config.servoStaticDict[servoName]
    verboseState = 1 if state else 0
    msg = f"7,{servoStatic.pin},{verboseState}\n"
    sendArduinoCommand(servoStatic.arduino, msg)


def requestRest(servoName):
    servoStatic = config.servoStaticDict[servoName]
    #servoControl.setPowerPin([servoStatic.powerPin])
    if servoStatic.enabled:
        pos = config.evalPosFromDeg(servoName, servoStatic.restDeg)
        requestServoPosition(servoName, pos, 1500)


def requestAllServosRest():
    config.log(f"all servos rest requested")
    for servoName, servoStatic in config.servoStaticDict.items():
        if servoStatic.enabled:
            #servoControl.setPowerPin([servoStatic.powerPin])
            pos = config.evalPosFromDeg(servoName, servoStatic.restDeg)
            requestServoPosition(servoName, pos, 1500)


def pinHigh(pinList):
    pins = "".join(c for c in str(pinList) if c not in '[ ]')
    msg = f"h,{pins}\n"
    config.log(f"arduino send pinHigh {msg}", publish=False)
    sendArduinoCommand(0, msg)


def pinLow(pinList):
    pins = "".join(c for c in str(pinList) if c not in '[ ]')
    msg = f"l,{pins}\n"
    config.log(f"arduino send pinLow {msg}", publish=False)
    sendArduinoCommand(0, msg)
