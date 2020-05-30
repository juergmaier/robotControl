# noinspection PyBroadException,SpellCheckingInspection

import time
import threading
import serial
import socket
import logging
import os
import shutil

from rpyc.utils.server import ThreadedServer
from PyQt5.QtWidgets import QApplication

import inmoovGlobal
import config
import arduinoSend
import arduinoReceive
import rpcReceive
import rpcSend
import threadWatchConnections
import guiLogic
import ik
import i01

#sys.path.append("../camImages")
import camImages

import stickFigure


clients = []
gestureDir = 'c:/projekte/inmoov/robotControl/marvinGestures'  # change this to marvinGestures once all gestures are verified


def openSerial(a):
    #{'arduinoIndex', 'arduinoName', 'comPort', 'connected'}

    if a['comPort'] == "unassigned":
        return True
    conn = None
    try:
        conn = serial.Serial(a['comPort'])
        # try to reset the arduino
        conn.setDTR(False)
        time.sleep(0.2)
        conn.setDTR(True)
        conn.baudrate = 115200
        conn.writeTimeout = 0
        #config.log(f"serial connection with arduino {a['arduinoIndex']}, {a['arduinoName']} on {a['comPort']} initialized")
        config.setSerialConnection(a['arduinoIndex'], conn)
        return True

    except Exception as e:
        config.log(f"exception on serial connect with arduino: {a['arduinoName']}, comPort: {a['comPort']}, {e}, going down")
        os._exit(1)


def arduinoReady(a):

    # check for response from arduino
    for i in range(3):
        time.sleep(2)
        arduinoSend.requestArduinoReady(a['arduinoIndex'])
        config.log(f"... wait for response from arduino {a['arduinoIndex']}, {a['arduinoName']}")

        timeout = time.time() + 5
        while not a['connected']:
            if time.time() > timeout:
                break  # from while
            else:
                time.sleep(0.5)

        if a['connected']:
            return True
        '''
        else:
            config.log(f"no response from arduino {a['arduinoIndex']}, {a['arduinoName']}, {a['comPort']}, retry serial connection set up")
            time.sleep(5)
            conn = config.arduinoConn[a['arduinoIndex']]
            if conn is not None:
                conn.close()
            config.setSerialConnection(a['arduinoIndex'], None)
            time.sleep(2)
        '''
    return False


def assignServos(arduinoIndex):
    '''
    servo definitions are stored in a json file
    for each servo handled by the <arduinoIndex> send the definitions to the arduino
    :param arduinoIndex:
    :return:
    '''

    config.log(f"send servo definitions to arduino and set current position to last persisted position")

    # send servo definition data to arduino and move to rest position
    for servoName, servoStatic in config.servoStaticDict.items():

        if servoStatic.enabled and servoStatic.arduino == arduinoIndex:

            #config.log(f"servo assign {servoName}")
            arduinoSend.servoAssign(servoName, config.getPersistedServoPosition(servoName))
            time.sleep(0.1)

    config.log(f"servo assign done")

    config.log("--")
    '''
    config.log(f"move enabled servos to rest position")
    DURATION_FOR_MOVE_TO_REST_POSITION = 1500

    for servoName, servoStatic in config.servoStaticDict.items():

        if servoStatic.enabled and servoStatic.arduino == arduinoIndex:

            pos = config.evalPosFromDeg(servoName, servoStatic.restDeg)
            #config.log(f"servo: {servoName}, restDeg: {servoStatic.restDeg}, pos: {pos}")
            arduinoSend.requestServoPosition(servoName, pos, DURATION_FOR_MOVE_TO_REST_POSITION)
            time.sleep(0.1)

    time.sleep(DURATION_FOR_MOVE_TO_REST_POSITION/1000 + 0.1)
    config.log(f"servo move to rest pos done")

    config.persistServoPositions()
    '''

def clearPowerPin(pinList):
    pinsToChange = []
    for pin in pinList:
        i = pin - config.powerPinOffset
        if config.powerPinState[i]:
            config.powerPinState[i] = False
            pinsToChange.append(pin)

    if len(pinsToChange) > 0:
        arduinoSend.pinLow(pinsToChange)


def setPowerPin(pinList):
    pinsToChange = []
    for pin in pinList:
        i = pin - config.powerPinOffset
        if not config.powerPinState[i]:
            config.powerPinState[i] = True
            pinsToChange.append(pin)

    if len(pinsToChange) > 0:


        arduinoSend.pinHigh(pinsToChange)


def checkOrCreateAllGesturesModule():

    if os.path.isfile('allGestures.py'):
        return

    with open('allGestures.py', 'w') as wfd:

        wfd.writelines("import time\n")
        wfd.writelines("import config\n")
        wfd.writelines("import i01\n")
        wfd.writelines("import ear\n")
        wfd.writelines("\n")
        wfd.writelines("isNeopixelActivated = False\n")
        wfd.writelines("\n")

        for item in os.listdir(gestureDir):
            file = gestureDir + "/" + item
            config.log(f"adding file to allGestures: {item}")
            with open(file, 'r') as fd:
                shutil.copyfileobj(fd, wfd)
                wfd.writelines("\n")
                wfd.writelines("\n")

    #importlib.reload(allGestures)


def initServoControl():

    config.log("load servo data")
    config.loadServoDefinitions()
    #createServoAllObjects()
    ik.init()
    config.loadServoPositions()

    # try to open comm ports
    for a in config.arduinoData:
        if not openSerial(a):
            config.log(f"could not open serial port {a['comPort']}, going down")
            os._exit(1)

    # start serial port receiving threads
    for a in config.arduinoData:

        serialReadThread = threading.Thread(target=arduinoReceive.readMessages, args={a['arduinoIndex']})
        serialReadThread.name = f"arduinoRead_{a['arduinoIndex']}"
        serialReadThread.start()

    # check for incoming messages from Arduino
    for a in config.arduinoData:

        # arduinoReady checks for incoming response from Arduino
        if arduinoReady(a):
            config.log(f"response from {a['comPort']} received")

    # without connection to arduino stop task
    for a in config.arduinoData:
        if not a['connected']:
            config.log(f"could not get a response from {a['comPort']}, going down")
            os._exit(1)

    for a in config.arduinoData:
        assignServos(a['arduinoIndex'])

    config.log(f"robotControl ready")
    rpcSend.publishBasicData()

    config.serverReady = True
    rpcSend.publishServerReady()

    time.sleep(2)   # time to update


def initCameras():
    '''
    def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, numReads):
    :return:
    '''
    try:
        camImages.cams.update({inmoovGlobal.EYE_CAM: camImages.UsbCamera("eyecam", 1, 640, 480, 18, 26, -90, 2)})
        config.log(f"connected with EYE_CAM")
        try:
            config.eyecamFrame = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()
        except Exception as e:
            config.log(f"could not capture frame from EYE_CAM  {e}")
            return False

        if config.eyecamFrame is None:
            return False

        return True

    except Exception as e:
        config.log(f"problem connecting EYE_CAM")
        return False
    # cams[inmoovGlobal.EYE_CAM].takeImage(True)



if __name__ == '__main__':

    config.pcName = socket.gethostname()
    config.pcIP = socket.gethostbyname(config.pcName)

    ##########################################################
    # initialization
    # Logging, renaming old logs for reviewing ...
    baseName = f"log/{config.serverName}"
    oldName = f"{baseName}9.log"
    if os.path.isfile(oldName):
        os.remove(oldName)
    for i in reversed(range(9)):
        oldName = f"{baseName}{i}.log"
        newName = f"{baseName}{i+1}.log"
        if os.path.isfile(oldName):
            os.rename(oldName, newName)
    oldName = f"{baseName}.log"
    newName = f"{baseName}0.log"
    if os.path.isfile(oldName):
        try:
            os.rename(oldName, newName)
        except Exception as e:
            config.log(f"can not rename {oldName} to {newName}")

    logging.basicConfig(
        filename=f"log/{config.serverName}.log",
        level=logging.INFO,
        format='%(message)s',
        filemode="w")

    config.log(f"{config.serverName} started")

    if not initCameras():
        config.log(f"could not connect with all cams, going down")
        exit()

    checkOrCreateAllGesturesModule()

    initServoControl()

    # just for testing face tracking
    #arduinoSend.setVerbose('head.neck', True)
    #arduinoSend.setVerbose('head.rothead', True)

    arduinoSend.requestAllServosRest()

    # START THREADS
    # starting rpyc connection watchdog
    watchDog = threading.Thread(target=threadWatchConnections.watchDog, args={})
    watchDog.name = "watchDog"
    watchDog.start()
    config.log(f"started thread for watching connections")

    config.log(f"start listening on port {config.MY_RPC_PORT}")
    server = ThreadedServer(rpcReceive.rpcListener(), port=config.MY_RPC_PORT, protocol_config={'allow_public_attrs': True})
    rpycThread = threading.Thread(target=server.start)
    rpycThread.name = "rpycListener"
    rpycThread.start()

    # start thread for lips movement
    config.log("guiLogic.init, adding thread MoveLips")
    lipsThread = threading.Thread(name="lipsThread", target = i01.MoveLipsThread)
    lipsThread.start()

    config.log(f"start gui in main thread")

    app = QApplication([])
    ''' try to move to init
    # add on_valueChanged and on_sliderReleased functions
    # for all servo sliders below the buttons
    for servoName in config.servoStaticDict:
        sliderName = servoName.replace('.','_') + 'Slider'
        addValueChangedFunctionToClass(f'on_{sliderName}_valueChanged', servoGui)
        addSliderReleasedFunctionToClass(f'on_{sliderName}_sliderReleased', servoGui)
    '''
    window = guiLogic.ServoGui()
    app.exec()


    # main needs to run the stick figure
    #ik.updateDhChain()
    #stickFigure.showRobot()
