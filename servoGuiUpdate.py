
import time

from PyQt5 import QtCore

import config
import arduinoSend

# work on update messages of servos

class GuiUpdateThread(QtCore.QThread):
    """
    This checks for new data in the guiUpdateQueue
    the queue can have different types of data based on the type attribute
    """

    # signal for gui update
    # raises guiLogic.updateGui
    updateGui = QtCore.pyqtSignal(int, int)

    def __init__(self):
        QtCore.QThread.__init__(self)


    def run(self):

        time.sleep(2)       # wait for gui to startup
        #config.setUpdateRunning(False)

        while True:
            #if config.getUpdateRunning():
            #    time.sleep(0.01)
            #    continue
            time.sleep(0.01)
            updateData = config.getOldestUpdateMessage()

            if updateData is not None:

                #config.log(f"updateData from queue: {updateData}")
                # check for unexpected data
                try:
                    type = updateData['type']
                except Exception as e:
                    config.log(f"msg from queue without a type {updateData}")
                    continue

                if updateData['type'] == config.SERVO_UPDATE:

                    servoName = updateData['servoName']

                    #config.log(f"servoUpdate {updateData['servoName']}, pos: {updateData['position']}")
                    if 0 > updateData['position'] > 180:
                        config.log(f"unreasonable position in update message")
                        return

                    #Data = {'type', 'assigned', 'moving', 'detached', 'position', 'degree'}
                    servoStatic = config.servoStaticDict[servoName]
                    servoDerived = config.servoDerivedDict[servoName]

                    if servoStatic is None:
                        config.log(f"could not eval servoDefinitions for {servoName}")
                        return

                    del updateData['type']  # remove added type
                    del updateData['servoName']  # remove added servo name

                    # update the local servo store
                    config.updateServoCurrent(servoName, updateData)

                    # inform the gui about the changed servo information using the unique servoId
                    self.updateGui.emit(config.SERVO_UPDATE, servoDerived.servoUniqueId)



                elif updateData['type'] == config.ARDUINO_UPDATE:
                        config.log("process arduino message from updateQueue")
                        if updateData['connected']:
                            self.updateGui.emit(config.ARDUINO_UPDATE, updateData['arduino'])


