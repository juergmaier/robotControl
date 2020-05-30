
import time
import random

from PyQt5.QtCore import pyqtSlot, QRunnable

import config
import arduinoSend



class RandomMovesThread(QRunnable):
    """
    This thread moves all robot servos with random speed and position
    """
    lastAction = time.time()
    moveFactor = 0.7            # the smaller the shorter the moves

    def moveServos(self):

        for servoName, curr in config.servoCurrentDict.items():

            if not curr.moving:
                servoStatic: config.cServoStatic = config.servoStaticDict[servoName]
                if servoStatic.minPos < servoStatic.maxPos:
                    pos = int(random.randint(servoStatic.minPos, servoStatic.maxPos) * self.moveFactor)
                else:
                    pos = int(random.randint(servoStatic.maxPos, servoStatic.minPos) * self.moveFactor)

                duration = random.randint(500, 3000)

                # prevent inward moves with armRotate as they might cause collisions of arms with body
                if servoName == 'leftArm.rotate':
                    if pos < 90:
                        pos = 90
                if servoName == 'rightArm.rotate':
                    if pos < 90:
                        pos = 90

                config.log(f"move servo {servoName}, pos: {pos}, duration: {duration}")
                arduinoSend.requestServoPosition(servoName, pos, duration)


    def run(self):

        while config.randomMovesActive: # controlled by the gui

            maxMoveSeconds = 20
            restSeconds = 8
            lastRest = time.time()
            while config.randomMovesActive:

                nextAction = random.randint(1000, 4000)

                if time.time() - self.lastAction > (nextAction/1000):

                    self.moveServos()

                    self.lastAction = time.time()

                time.sleep(0.1)

                if time.time() - lastRest > maxMoveSeconds:
                    config.log("pause in random moves")
                    arduinoSend.requestAllServosRest()
                    time.sleep(restSeconds)
                    config.log("continue random moves")
                    lastRest = time.time()
