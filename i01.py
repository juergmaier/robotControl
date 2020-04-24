import time
import config

from PyQt5 import QtCore

import pyttsx3

import allGestures
import arduinoSend


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



class MoveLipsThread(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.mouthOpen = "aehij"
        self.mouthClosed = "bmp "

    def run(self):
        config.log(f"move lips thread started")
        secondsPerChar = 0.055
        self.servoStatic = config.servoStaticDict['head.jaw']
        self.lastMouthPosition = self.servoStatic.minPos

        while True:

            if config.lipsText is None:
                time.sleep(0.1)
                continue

            for charPos in range(len(config.lipsText)):
                #config.log(f"char to speak: {self.text[charPos]}")

                # check for modified lipsText
                if charPos >= len(config.lipsText):
                    continue

                # tts needs some time to start speaking
                if charPos == 0:
                    config.log(f"text to speak: {config.lipsText}")
                    time.sleep(0.5)

                # mouth default half open
                mouthServoPos = (self.servoStatic.maxPos + self.servoStatic.minPos) / 2

                # check for character spoken with mouth open
                if config.lipsText[charPos] in self.mouthOpen:
                    mouthServoPos = self.servoStatic.maxPos

                # check for character spoken with mouth closed
                if config.lipsText[charPos] in self.mouthClosed:
                    mouthServoPos = self.servoStatic.minPos

                # check for changed mouth position
                if mouthServoPos != self.lastMouthPosition:
                    moveDuration = 50
                    arduinoSend.requestServoPosition("head.jaw", mouthServoPos, moveDuration, filterSequence=False)
                    self.lastMouthPosition = mouthServoPos

                time.sleep(secondsPerChar)

            # close mouth after speaking
            arduinoSend.requestServoPosition("head.jaw", self.servoStatic.minPos, 100, filterSequence=False)
            self.lastMouthPosition = self.servoStatic.minPos
            config.lipsText = None


class Mouth:

    def __init__(self):
        self.engine = pyttsx3.init()
        '''
        German voice Karsten existed only in Speech_OneCore folder.
        Needed to export the registry-entry of the voice, change the path to \Speech\ with text editor
        and reimport the .reg file. After reboot the voice was selectable
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print(voice.id)
            self.engine.setProperty('voice', voice.id)
            self.engine.say('stimme')
        self.engine.runAndWait()
        '''
        voiceId = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_deCH_Karsten"
        self.engine.setProperty('voice', voiceId)
        rate = self.engine.getProperty('rate')      # default = 200 words per minute
        self.engine.setProperty('rate', rate - 30)


    def speakBlocking(self, text):
        #config.log(f"speak: {text}, {len(text)} chars")
        speechStart = time.time()
        self.engine.say(text)

        config.lipsText = text      # triggers lips movement in moveLipsThread

        self.engine.runAndWait()
        #config.log(f"speech finished after: {time.time()-speechStart:.1f} s, charPerSec: {(time.time()-speechStart)/len(text):.2f}")


    def speak(self, text):
        print(text)
        self.engine.say(text)


mouth = Mouth()



class LeftArm:
    class Omoplate():
        def enableAutoDisable(self, newState):
            pass

leftArm = LeftArm()
leftArm.omoplate = leftArm.Omoplate()

class RightArm:
    class Omoplate():
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
