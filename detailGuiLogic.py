
import time


from PyQt5 import uic, QtCore, QtWidgets

import config
import detailQtGui
import arduinoSend


class detailGui(QtWidgets.QDialog, detailQtGui.Ui_ServoDetails):

    def __init__(self):
        super().__init__()
        self.title = 'my dialog'
        #self.setupUi(self)
        uic.loadUi('servoDetailGui.ui', self)

        self.servoType = ""
        self.servoName = ""

    def initUI(self, servoName):
        servoStatic: config.ServoStatic = config.servoStaticDict[servoName]
        self.servoName = servoName
        self.setWindowTitle(servoName)
        self.Arduino.setValue(servoStatic.arduino)
        self.Pin.setValue(servoStatic.pin)
        self.PowerPin.setValue(servoStatic.powerPin)
        self.Enabled.setChecked(servoStatic.enabled)
        self.MinComment.setText(servoStatic.minComment)
        self.MaxComment.setText(servoStatic.maxComment)
        self.MinPos.setValue(servoStatic.minPos)
        self.MaxPos.setValue(servoStatic.maxPos)
        self.ZeroDegPos.setValue(servoStatic.zeroDegPos)
        self.MinDegrees.setValue(servoStatic.minDeg)
        self.MaxDegrees.setValue(servoStatic.maxDeg)
        self.AutoDetach.setValue(servoStatic.autoDetach)
        self.Inverted.setChecked(servoStatic.inverted)
        self.RestDegrees.setValue(servoStatic.restDeg)
        ####
        #self.ServoType
        servoTypeList = []

        # populate drop down with servoTypes
        for t in config.servoTypeDict:
            self.ServoType.addItem(t)
        index = self.ServoType.findText(servoStatic.servoType, QtCore.Qt.MatchFixedString)
        self.ServoType.setCurrentIndex(index)
        self.servoType = servoStatic.servoType
        self.ServoType.activated[str].connect(self.servoTypeChoice)

        self.MoveSpeed.setValue(servoStatic.moveSpeed)
        self.TerminalSlot.setValue(servoStatic.cableTerminal)
        self.CableArduinoTerminal.setText(servoStatic.wireColorArduinoTerminal)
        self.CableTerminalServo.setText(servoStatic.wireColorTerminalServo)

        self.buttonBox.accepted.connect(self.save)

    def servoTypeChoice(self, selection):
        self.servoType = selection

    def save(self):
        servoStatic: config.ServoStatic = config.servoStaticDict[self.servoName]
        servoStatic.arduino = self.Arduino.value()
        servoStatic.pin = self.Pin.value()
        servoStatic.powerPin = self.PowerPin.value()
        servoStatic.enabled = self.Enabled.isChecked()
        servoStatic.minComment = self.MinComment.text()
        servoStatic.maxComment = self.MaxComment.text()
        servoStatic.minPos = self.MinPos.value()
        servoStatic.maxPos = self.MaxPos.value()
        servoStatic.zeroDegPos = self.ZeroDegPos.value()
        servoStatic.minDeg = self.MinDegrees.value()
        servoStatic.maxDeg = self.MaxDegrees.value()
        servoStatic.autoDetach = self.AutoDetach.value()

        config.log(f"new autoDetach: {self.AutoDetach.value()}")
        config.log(f"servoStatic autoDetach: {servoStatic.autoDetach}")

        servoStatic.inverted = self.Inverted.isChecked()
        servoStatic.restDeg = self.RestDegrees.value()
        servoStatic.servoType = self.ServoType.currentText()
        servoStatic.moveSpeed = self.MoveSpeed.value()
        servoStatic.cableTerminal = self.TerminalSlot.value()
        servoStatic.wireColorArduinoTerminal = self.CableArduinoTerminal.text()
        servoStatic.wireColorTerminalServo = self.CableTerminalServo.text()

        config.servoStaticDict[self.servoName] = servoStatic
        config.marvinShares.updateServoStaticDict(self.servoName, servoStatic)

        # update derived servo values too
        servoDerived = config.ServoDerived(self.servoName)
        config.servoDerivedDict.update({self.servoName: servoDerived})

        # update arduino too
        arduinoSend.servoAssign(self.servoName, config.getPersistedServoPosition(self.servoName))
        config.log(f"updated servo definitions for {self.servoName}")
        config.saveServoStaticDict()

