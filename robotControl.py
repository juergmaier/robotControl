# noinspection PyBroadException,SpellCheckingInspection

import sys
import time
import threading
import serial
import socket
import logging
import os
import shutil


from PyQt5.QtWidgets import QApplication

import inmoovGlobal
import config
import arduinoSend
import arduinoReceive
import rpcSend
import guiLogic
import ik
import i01
import marvinShares
import speaker
import servoRequests

#sys.path.append("../camImages")
import camImages


clients = []
# change this to marvinGestures once all gestures are verified
gestureDir = 'c:/projekte/inmoov/robotControl/marvinGestures'


def openSerial(a):
    #{'arduinoIndex', 'arduinoName', 'comPort', 'connected'}

    if a['comPort'] == "unassigned":
        return True
    conn = None
    try:
        conn = serial.Serial(a['comPort'])
        # try to reset the arduino
        #conn.setDTR(False)
        #time.sleep(0.2)
        #conn.setDTR(True)
        conn.baudrate = 115200
        conn.writeTimeout = 0
        #config.log(f"serial connection with arduino {a['arduinoIndex']}, {a['arduinoName']} on {a['comPort']} initialized")
        config.setSerialConnection(a['arduinoIndex'], conn)
        return True

    except Exception as eSerial:
        config.log(f"exception on serial connect with arduino: {a['arduinoName']}, comPort: {a['comPort']}, {eSerial}, going down")
        if conn is not None:
            try:
                conn.close()
            except Exception as e2:
                config.log(f"conn.close failed, {e2}")
        sys.exit(1)


def assignServos(arduinoIndex):
    """
    servo definitions are stored in a json file
    for each servo handled by the <arduinoIndex> send the definitions to the arduino
    :param arduinoIndex:
    :return:
    """

    config.log(f"send servo definitions to arduino {arduinoIndex} and set current position to last persisted position")

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
    time.sleep(0.5)
    for a in config.arduinoData:
        arduinoSend.requestArduinoReady(a['arduinoIndex'])

    # wait for response from arduinos
    for i in range(10):
        if config.arduinoData[0]['connected'] and config.arduinoData[1]['connected']:
            break
        time.sleep(0.5)

    # check for connection
    for a in config.arduinoData:
        if not a['connected']:
            config.log(f"could not receive serial response from arduino {a['arduinoName']}, {a['comPort']}")
            conn = config.arduinoConn[a['arduinoIndex']]
            if conn is not None:
                try:
                    conn.close()
                except Exception as e2:
                    config.log(f"conn.close failed, {e2}")
            sys.exit(1)

    for a in config.arduinoData:
        assignServos(a['arduinoIndex'])

    # set verbose mode for servos to report more details
    arduinoSend.setVerbose('head.rothead', True)

    config.log(f"robotControl ready")
    #rpcSend.publishBasicData()

    #config.serverReady = True
    #rpcSend.publishServerReady()

    #time.sleep(2)   # time to update


def initCameras():
    '''
    def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, numReads):
    :return:
    '''
    try:
        # def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, numReads):'
        camImages.cams.update({inmoovGlobal.EYE_CAM: camImages.UsbCamera("eyecam", 2, 640, 480, 18, 26, -90, 5)})
        config.log(f"connected with EYE_CAM")
        try:
            image = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()   # camera initialization
        except Exception as e:
            config.log(f"could not capture frame from EYE_CAM  {e}")
            return False

        if image is None:
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

    config.log("start thread marvinShares")
    config.marvinShares = marvinShares.MarvinShares()
    config.marvinShares.start()
    #time.sleep(2)

    # start thread for lips movement
    config.log("start thread MoveLips")
    lips = speaker.MoveLips()
    lipsThread = threading.Thread(name="lipsThread", target = lips.run, args={})
    lipsThread.start()

    config.log("start thread speaker")
    speaker = speaker.Speaker() #config.marvinShares.speakRequests)
    speakerThread = threading.Thread(name="speakerThread", target=speaker.run, args={})
    speakerThread.start()

    i01.mouth.speakBlocking("sprachserver gestartet")
    #config.marvinShares.speechRequests.put("sprachserver gestartet")

    config.log(f"start servoRequests thread")
    servoRequestsThread = threading.Thread(name="servoRequests", target=servoRequests.processServoRequests, args={})
    servoRequestsThread.start()


    # just for testing face tracking
    #arduinoSend.setVerbose('head.neck', True)
    #arduinoSend.setVerbose('head.rothead', True)

    arduinoSend.requestAllServosRest()

    # START THREADS
    # starting rpyc connection watchdog
    #watchDog = threading.Thread(target=threadWatchConnections.watchDog, args={})
    #watchDog.name = "watchDog"
    #watchDog.start()
    #config.log(f"started thread for watching connections")

    #config.log(f"start listening on port {config.MY_RPC_PORT}")
    #server = ThreadedServer(rpcReceive.rpcListener(), port=config.MY_RPC_PORT, protocol_config={'allow_public_attrs': True})
    #rpycThread = threading.Thread(target=server.start)
    #rpycThread.name = "rpycListener"
    #rpycThread.start()

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
