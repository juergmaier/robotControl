
import time
from multiprocessing.managers import SyncManager
import pyttsx3

import config
import arduinoSend

class QueueManager(SyncManager): pass

class Speaker():
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

        #self.engine.runAndWait()

    def run(self):

        config.log(f"speaker started")

        #self.engine = pyttsx3.init()        # may be necessary

        while True:
            text = config.marvinShares.speechRequests.get()

            config.log(f"tts request: {text}")

            speechStart = time.time()

            config.lipsText = text      # triggers lips movement in moveLipsThread
            self.engine.say(text)
            self.engine.runAndWait()

            # signal speach done
            config.marvinShares.speechResponds.put("done")
            config.log(f"speech responds signaled after: {time.time()-speechStart:.1f} s, charPerSec: {(time.time()-speechStart)/len(text):.2f}")


class MoveLips():

    def __init__(self):
        super().__init__()
        #QtCore.QThread.__init__(self)
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
                    config.log(f"text for lip movement: {config.lipsText}")
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

