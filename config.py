

import datetime
import simplejson as json
import os
import time
import logging
#from collections import deque
import queue

import rpcSend
import robotControl

numArduinos = 2
arduinoData = [{'arduinoIndex': 0, 'arduinoName': 'left', 'comPort': 'COM8', 'connected': False},
               {'arduinoIndex': 1, 'arduinoName': 'right', 'comPort': 'COM4', 'connected': False}]
arduinoConn = [None] * numArduinos

numServos = 0

SERVO_UPDATE = 0
ARDUINO_UPDATE = 1
CONNECTION_UPDATE = 2

pcName = None
pcIP = None
MY_RPC_PORT = 20004

serverName = 'robotControl'
serverReady = False

guiUpdateQueue = queue.Queue(100)  # deque(maxlen=None) dequeue is not thread safe

SERVO_STATIC_DEFINITIONS_FILE = 'servoStaticDefinitions.json'
SERVO_TYPE_DEFINITIONS_FILE = 'servoTypeDefinitions.json'
PERSISTED_SERVO_POSITIONS_FILE = 'persistedServoPositions.json'

servoStaticDict = {}    # the static definitions of all servos from the json file
servoTypeDict = {}      # servo properties given by manufacturer
servoDerivedDict = {}   # useful derived values for servo accessible by servoDerivedDict[<servoName>]
servoCurrentDict = {}   # all dynamic servo values accessible by servoCurrentDict[<servoName>]


REST_MOVE_DURATION = 1500
SWIPE_MOVE_DURATION = 1500
swipingServoName = None
swipeDuration = 0
nextSwipePos = 0
randomMovesActive = False
gestureRunning = False
gestureName = None

lipsText = None

servoNameByArduinoAndPin = {}   # a list to access servos by Arduino and Id

powerPinOffset = 40
powerPinState = [False] * 8

persistedServoPositions = {}
lastPositionSaveTime = time.time()

clientList = []

connectionWatchInterval = 5

simulateServoMoves = False

verbose = False


'''
Information about the servos is kept in classes. 
The instances are kept in dictionaries and are accessible by servoName
The objects are:
cServoStatic:   robot specific definitions about the servo use
    "arduino": 0,
    "pin": 10,
    "powerPin": 40,
    "minComment": "rotate left (out)",
    "maxComment": "rotate right (in)",
    "minPos": 0,
    "maxPos": 180,
    "zeroDegPos": 90,
    "minDeg": -60,
    "maxDeg": 60,
    "autoDetach": 1000,
    "inverted": false,
    "restDeg": 0,
    "enabled": true,
    "servoType": "HS-805",
    "moveSpeed": 500,
    "cableTerminal": 5,
    "wireColorArduinoTerminal": "grey",
    "wireColorTerminalServo": "BROWN/white"
    
cServoType:     manufacture specific definitions of the servo

cServoDerived:  intermediate useful values 
'''

class cServoStatic:
    def __init__(self, servoDefinition):
        self.__dict__ = servoDefinition


class cServoType:
    def __init__(self, servoTypeDefinition):
        self.__dict__ = servoTypeDefinition


class cServoDerived:
    '''
    Useful preevaluated values with servo
    '''
    def __init__(self, servoName):

        servoStatic = servoStaticDict[servoName]
        servoType = servoTypeDict[servoStatic.servoType]

        self.servoUniqueId = (servoStatic.arduino*100) + servoStatic.pin
        self.degRange = servoStatic.maxDeg - servoStatic.minDeg
        self.posRange = servoStatic.maxPos - servoStatic.minPos

        # a servo has normally a shaft rotation speed for a 60° swipe defined
        # this is the maximum speed possible by the servo
        # the inmoov robot has in many cases not a direct shaft connection for a movement
        # but a mechnical gear mechanism
        # for these servos we can define a max move speed of the controlled part
        # msPerPos uses the move speed if it is slower than the servo speed
        # robotControl checks requested move durations against the max speed possible and
        # increases move duration if necessary
        # ATTENTION: servoTypeSpeed is s/60 deg, moveSpeed is ms/60 deg!!
        if (servoStatic.moveSpeed/1000) > servoType.typeSpeed:
            self.msPerPos = servoStatic.moveSpeed / 60
        else:
            self.msPerPos = servoType.typeSpeed * 1000 / 60


class cServoCurrent:
    '''
    cServoCurrent:  the current status and position of the servo
        servoName
        assigned
        moving
        attached
        autoDetach
        verbose
        position
        degrees
        timeOfLastMoveRequest
    '''
    def __init__(self, servoName):
        self.servoName = servoName
        self.assigned = False
        self.moving = False
        self.attached = False
        self.autoDetach = 1.0
        self.verbose = False
        self.position = 0
        self.degrees = 0
        self.timeOfLastMoveRequest = time.time()

    def updateData(self, newDegrees, newPosition, newAssigned, newMoving, newAttached, newAutoDetach,
                            newVerbose):
        self.degrees = newDegrees
        self.position = newPosition
        self.assigned = newAssigned
        self.moving = newMoving
        self.attached = newAttached
        self.autoDetach = newAutoDetach
        self.verbose = newVerbose


class objectview(object):
    """
    allows attibs of a dict to be accessed with dot notation
    e.g.
    mydict={'a':1,'b':2}
    oMydict = objectview(mydict)
    then instead of mydict['a'] we can write mydict.a
    """
    def __init__(self, d):
        self.__dict__ = d


def loadServoDefinitions():
    global servoStaticDict

    log("loading servo definitions")
    try:
        with open(SERVO_STATIC_DEFINITIONS_FILE, 'r') as infile:
            servoStaticDefinitions = json.load(infile)
        # if successfully read create a backup just in case
        with open(SERVO_STATIC_DEFINITIONS_FILE + ".bak", 'w') as outfile:
            json.dump(servoStaticDefinitions, outfile, indent=2)

    except Exception as e:
        log(f"missing {SERVO_STATIC_DEFINITIONS_FILE} file, try using the backup file")
        os._exit(2)

    log("loading servo types")
    try:
        with open(SERVO_TYPE_DEFINITIONS_FILE, 'r') as infile:
            servoTypeDefinitions = json.load(infile)
        with open(SERVO_TYPE_DEFINITIONS_FILE + ".bak", 'w') as outfile:
            json.dump(servoTypeDefinitions, outfile, indent=2)

    except Exception as e:
        log(f"missing {SERVO_TYPE_DEFINITIONS_FILE} file, try using the backup file")
        os._exit(3)


    for servoTypeName, servoTypeData in servoTypeDefinitions.items():
        servoType = cServoType(servoTypeData)
        servoTypeDict.update({servoTypeName: servoType})

    for servoName in servoStaticDefinitions:

        servoStatic = cServoStatic(servoStaticDefinitions[servoName])
        servoType = servoTypeDict[servoStatic.servoType]

        # data cleansing
        # BE AWARE: inversion is handled in the arduino only, maxPos > minPos is a MUST!
        # check for valid min/max position values in servo type definition
        if servoType.typeMaxPos < servoType.typeMinPos:
            log(f"wrong servo type values, typeMaxPos < typeMinPos, servo disabled")
            servoStatic.enabled = False

        # check for valid min/max degree values in servo definition
        if servoStatic.maxDeg < servoStatic.minDeg:
            log(f"wrong servo min/max values, maxDeg < minDeg for {servoName}, servo disabled")
            servoStatic.enabled = False

        # check for servo values in range of servo type definition
        if servoStatic.minPos < servoType.typeMinPos:
            log(f"servo min pos lower than servo type min pos for {servoName}, servo min pos adjusted")
            servoStatic.minPos = servoType.typeMinPos

        if servoStatic.maxPos > servoType.typeMaxPos:
            log(f"servo max pos higher than servo type max pos for {servoName}, servo max pos adjusted")
            servoStatic.maxPos = servoType.typeMaxPos

        # add objects to the servoDictionaries
        servoStaticDict.update({servoName: servoStatic})

        servoDerived = cServoDerived(servoName)
        servoDerivedDict.update({servoName: servoDerived})

        # create a dict to find servo name from arduino and pin (for messages from arduino)
        servoNameByArduinoAndPin.update({servoDerived.servoUniqueId: servoName})


def log(msg, publish=True):

    logtime = str(datetime.datetime.now())[11:23]
    logging.info(f"{logtime} - {msg}")
    print(f"{logtime} - {msg}")

    if publish:
        rpcSend.publishLog(f"{serverName} - " + msg)


def setArduinoStatus(arduino, newStatus):

    global arduinoData

    arduinoData[arduino]['connected'] = newStatus


def setAutoDetach(servoStatic, newValue):

    servoStatic.autoDetach = newValue



def setSerialConnection(arduinoIndex, conn):

    global arduinoConn

    log(f"serial connection with arduino {arduinoIndex} set")
    arduinoConn[arduinoIndex] = conn


def getPersistedServoPosition(servoName):
    return persistedServoPositions[servoName]


def setUpdateRunning(state):
    global updateRunning
    updateRunning = state


def getUpdateRunning():
    return updateRunning


def evalDegFromPos(servoName: str, inPos: int):
    # inPos has to be in the 0..180 range (servo.write() limits this)
    # minPos has to be smaller than maxPos. Inversion is handled in the arduino
    # minDegrees always has to be smaller than maxDegrees
    servoDerived = servoDerivedDict[servoName]
    servoStatic = servoStaticDict[servoName]

    degPerPos = servoDerived.degRange / servoDerived.posRange
    deltaPos = inPos - servoStatic.zeroDegPos

    degrees = deltaPos * degPerPos
    #print(f"degrees: {degrees}")
    return round(degrees)


def evalPosFromDeg(servoName, inDeg):
    """
    a servo has min/max pos and deg defined. The 0 degree pos can be off center.
    :param servoStatic:
    :param inDeg:
    :return:
    """
    servoDerived = servoDerivedDict[servoName]
    servoStatic = servoStaticDict[servoName]

    posPerDeg = servoDerived.posRange / servoDerived.degRange
    pos = (inDeg * posPerDeg) + servoStatic.zeroDegPos
    return round(pos)


def getServoPosition(servoName):
    servoCurrent = servoCurrentDict[servoName]
    return servoCurrent.degrees, servoCurrent.position, servoCurrent.moving


def saveServoStaticDict():
    '''
    servoStaticDict is a dict of cServoStatic objects by servoName
    to store it in json revert the objects back to dictionaries
    :return:
    '''
    servoStaticDefinitions = {}
    for servoName, servoObject in servoStaticDict.items():
        servoStaticDefinitions.update({servoName: servoObject.__dict__})

    with open(SERVO_STATIC_DEFINITIONS_FILE, 'w') as outfile:
        json.dump(servoStaticDefinitions, outfile, indent=2)


def loadServoPositions():

    global persistedServoPositions, servoCurrentDict

    log("load last known servo positions")
    if os.path.isfile(PERSISTED_SERVO_POSITIONS_FILE):
        with open(PERSISTED_SERVO_POSITIONS_FILE, 'r') as infile:
            persistedServoPositions = json.load(infile)
            if len(persistedServoPositions) != len(servoStaticDict):
                log(f"mismatch of servoDict and persistedServoPositions")
                createPersistedDefaultServoPositions()
    else:
        createPersistedDefaultServoPositions()

    # check for valid persisted position
    for servoName in servoStaticDict:

        servoStatic = servoStaticDict[servoName]

        # try to assign the persisted last known servo position
        try:
            p = persistedServoPositions[servoName]
        except KeyError:
            # in case we do not have a last known servo position use 90 as default
            p = 90

        # set current position to min or max if outside range
        if p < servoStatic.minPos:
            p = servoStatic.minPos
        if p > servoStatic.maxPos:
            p = servoStatic.maxPos

        # create cServoCurrent object
        servoCurrent = cServoCurrent(servoName)

        servoCurrent.position = p

        # set degrees from pos
        servoCurrent.degrees = evalDegFromPos(servoName, p)

        # add object to servoCurrentDict with key servoName
        servoCurrentDict.update({servoName: servoCurrent})

    log("servoPositions loaded")


def persistServoPositions():

    global lastPositionSaveTime

    lastPositionSaveTime = time.time()
    with open(PERSISTED_SERVO_POSITIONS_FILE, 'w') as outfile:
        json.dump(persistedServoPositions, outfile, indent=2)


def saveServoPosition(servoName, position, maxDelay=10):
    '''
    save current servo position to json file if last safe time differs
    more than maxDelay seconds
    :param servoName:
    :param position:
    :param maxDelay:
    :return:
    '''

    persistedServoPositions[servoName] = position
    if time.time() - lastPositionSaveTime > maxDelay:
        persistServoPositions()


def createPersistedDefaultServoPositions():
    '''
    initialize default servo positions in case of missing or differing json file
    :return:
    '''

    global persistedServoPositions

    persistedServoPositions = {}
    for servoName in servoStaticDict:
        persistedServoPositions.update({servoName: 90})
    persistServoPositions()


def updateServoCurrent(servoName, servoData):
    '''
    servoCurrent is a list of cServoCurrent objects
    update the instance values with the data from the servoData dictionary
    :param servoName:
    :param servoData:
    :return:
    '''

    global servoCurrentDict

    for key, value in servoData.items():
        setattr(servoCurrentDict[servoName], key, value)
    #servoCurrent[servoName] = servoData

#
def getOldestUpdateMessage():
    if not guiUpdateQueue.empty():
        return guiUpdateQueue.get()
    else:
        return None

'''
def addToUpdateQueue(data):
    log(f"add to queue: {data}")
    guiUpdateQueue.put(data)
'''

def setRandomMovesActive(state):
    global randomMovesActive
    randomMovesActive = state
    log(f"random moves state: {state}")

