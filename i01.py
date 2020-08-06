import time
import config
#import queue
#import multiprocessing

from PyQt5.QtCore import pyqtSlot, QRunnable

import allGestures
import arduinoSend

'''
class GestureThread(QtCore.QThread):
    """
    This thread plays a gesture file
    """
    def __init__(self):
        QtCore.QThread.__init__(self)


    def run(self):

        while True:
            while not config.gestureRunning:
                time.sleep(1)
                continue

            config.log(f"starting gesture {config.gestureName}")
            callableFunction = getattr(allGestures, config.gestureName)
            callableFunction()
'''
class GesturePlay(QRunnable):
    @pyqtSlot()
    def run(self):

        while True:
            if not config.gestureRunning:
                time.sleep(1)
                continue

            config.log(f"starting gesture {config.gestureName}")
            callableFunction = getattr(allGestures, config.gestureName)
            callableFunction()


class LeftArm:
    class Omoplate:
        def enableAutoDisable(self, newState):
            pass

leftArm = LeftArm()
leftArm.omoplate = leftArm.Omoplate()

class RightArm:
    class Omoplate:
        def enableAutoDisable(self, newState):
            pass
rightArm = RightArm()
rightArm.omoplate = rightArm.Omoplate()


class Head:
    class Neck:
        def enableAutoDisable(self, newState):
            pass

    class EyeY:
        def moveTo(self, pos):
            arduinoSend.requestServoPosition('head.eyeY', int(pos), 500)

    class EyeX:
        def moveTo(self, pos):
            arduinoSend.requestServoPosition('head.eyeX', int(pos), 500)

    class RollNeck:
        def moveTo(self, pos):
            pass

head = Head()
head.neck = head.Neck()
head.eyeY = head.EyeY()
head.eyeX = head.EyeX()
head.rollNeck = head.RollNeck()


class Mouth:
    def __init__(self):
        pass

    def speakBlocking(self,text):
        config.log(f"speak blocking: {text}")
        config.marvinShares.speechRequests.put(text)
        #config.log(f"wait for text spoken")
        responseWaitStart = time.time()
        while config.marvinShares.speechResponds.empty():
            if time.time() - responseWaitStart > 3:
                break
            time.sleep(0.1)

mouth = Mouth()


# these functions are part of the gesture definitions, e.g. i01.moveArm
def startedGesture():
    pass


def finishedGesture():
    config.gesture = None
    config.gestureRunning = False



def moveArm(side,bicep,rotate,shoulder,omoplate):
    if not config.gestureRunning:
        return
    # requestServoPos(servoName, pos, duration):
    arduinoSend.requestServoPosition(side + 'Arm.bicep', int(bicep), allGestures.armMoveDuration[side + 'Arm.bicep']['current'] )
    arduinoSend.requestServoPosition(side + 'Arm.rotate', int(rotate), allGestures.armMoveDuration[side + 'Arm.rotate']['current'] )
    arduinoSend.requestServoPosition(side + 'Arm.shoulder', int(90-shoulder), allGestures.armMoveDuration[side + 'Arm.shoulder']['current'] )
    arduinoSend.requestServoPosition(side + 'Arm.omoplate', int(omoplate), allGestures.armMoveDuration[side + 'Arm.omoplate']['current'] )


def moveHand(side,thumb,index,majeure,ringFinger,pinky,wrist=90):
    if not config.gestureRunning:
        return
    # requestServoPos(servoName, pos, duration):
    arduinoSend.requestServoPosition(side + 'Hand.thumb', int(thumb), allGestures.handMoveDuration[side + 'Hand.thumb']['current'] )
    arduinoSend.requestServoPosition(side + 'Hand.index', int(index), allGestures.handMoveDuration[side + 'Hand.index']['current'] )
    arduinoSend.requestServoPosition(side + 'Hand.majeure', int(majeure), allGestures.handMoveDuration[side + 'Hand.majeure']['current'] )
    arduinoSend.requestServoPosition(side + 'Hand.ringFinger', int(ringFinger), allGestures.handMoveDuration[side + 'Hand.ringFinger']['current'] )
    arduinoSend.requestServoPosition(side + 'Hand.pinky', int(pinky), allGestures.handMoveDuration[side + 'Hand.pinky']['current'] )
    arduinoSend.requestServoPosition(side + 'Hand.wrist', int(wrist), allGestures.handMoveDuration[side + 'Hand.wrist']['current'] )


def setHandVelocity(side,thumb,index,majeure,ringFinger,pinky,wrist=90):
        pass


def setArmVelocity(side,b,r,s,o):
    pass


def setHeadVelocity(a,b,c=0,d=0,e=0):
    pass


def setTorsoVelocity(a,b,c=1):
    pass

def moveHead(rotheadPos, neckPos, mouth=30, eyeX=90, eyeY=90):
    if not config.gestureRunning:
        return
    #config.log(f'moveHead, rotHead: {rotheadPos}, neck: {neckPos}')
    arduinoSend.requestServoPosition('head.rothead', int(rotheadPos), int(allGestures.headMoveDuration['head.rothead']['current']))
    arduinoSend.requestServoPosition('head.neck', int(neckPos), int(allGestures.headMoveDuration['head.neck']['current']))


def moveTorso(topStomPos, midStomPos, lowStomPos):
    if not config.gestureRunning:
        return
    #config.log(f'moveTorso, topStom: {topStomPos}, midStom: {midStomPos}, lowStom: {lowStomPos}')
    arduinoSend.requestServoPosition('torso.topStom', int(topStomPos), int(allGestures.torsoMoveDuration['torso.topStom']['current']))
    arduinoSend.requestServoPosition('torso.midStom', int(midStomPos), int(allGestures.torsoMoveDuration['torso.midStom']['current']))
    #arduinoSend.requestServoPosition('torso.lowStom', int(lowStomPos), int(allGestures.torsoMoveDuration['torso.lowStom']['current']))


def rest():
    config.log(f"rest")
    arduinoSend.requestAllServosRest()


def giving():
    config.log(f"what is mrl giving() doing?")


def attach():
    pass

def detach():
    pass

def setNeopixelAnimation(theme, a, b, c, d):
    pass


def isCameraOn():
    return False
