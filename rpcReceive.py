import os
import time
import rpyc

import config
import arduinoSend
import simplejson as json
import rpcSend

class rpcListener(rpyc.Service):

    ############################## common routines for clients

    def on_connect(self, conn):
        print(f"on_connect seen {conn}")
        callerName = conn._channel.stream.sock.getpeername()
        print(f"caller: {callerName}")


    def exposed_requestForReplyConnection(self, ip, port, messages=[], interval=5):
        """

        :param ip:
        :param port:
        :param messages: list of names of messages the client is insterested in or empty list for all
        :param interval:
        :return:
        """

        messageList = list(messages)
        config.log(f"request for reply connection received from {ip}:{port}, messageList: {messageList}")
        myConfig = {"allow_all_attrs": True, "allow_pickle": True}
        try:
            replyConn = rpyc.connect(ip, port, config={'sync_request_timeout': 2})
        except Exception as e:
            config.log(f"failed to open a reply connection, {e}")
            return

        config.log(f"reply connection established")
        clientId = (ip, port)
        connectionUpdated = False
        for c in config.clientList:
            if c['clientId'] == clientId:
                config.log(f"update client connection")
                c['replyConn'] = replyConn
                c['lifeSignalReceived'] = time.time()
                connectionUpdated = True

        if not connectionUpdated:
            config.log(f"append client connection {clientId}")
            config.clientList.append({'clientId': clientId,
                                      'replyConn': replyConn,
                                      'lifeSignalReceived': time.time(),
                                      'messageList': messageList,
                                      'interval': interval})
            config.log(f"clientList: {config.clientList}")

        # if server is already running send a ready message
        if config.serverReady:
            rpcSend.publishBasicData()
            rpcSend.publishServerReady()
        else:
            rpcSend.publishLifeSignal(ip, port)

    ''' 16.12.2019 threadConnectionWatch sends life signal to all clients in intervals
    def exposed_requestLifeSignal(self, ip, port):

        #config.log(f"life signal request received from  {ip}, {port}")
        for c in config.clientList:
            if c['clientId'] == (ip, port):
                c['lifeSignalReceived'] = time.time()
        rpcSend.publishLifeSignal(ip, port)
    '''

    def exposed_terminate(self):
        print(f"{config.serverName} server - terminate request received")
        os._exit(0)
        return True

    def exposed_clientLifeSignal(self, ip, port):
        clientId = (ip,port)
        for c in config.clientList:
            if c['clientId'] == clientId:
                c['lifeSignalReceived'] = time.time()


    ############################## end common routines for clients

    def exposed_getServoDict(self):
        jsonMsg = ''
        leadingChar = '{'
        for servoName, o in config.servos.items():  # objectviews of the servoDefinitions (dict attribs accessible with . notation)
            jsonMsg += leadingChar + '"' + servoName + '":' + json.dumps(o.__dict__)
            leadingChar = ','
        jsonMsg += '}'
        return jsonMsg

    '''
    def exposed_getServoCurrentList(self):
        jsonMsg = ''
        leadingChar = '{'
        for servoName, o in config.servoCurrent.items():
            jsonMsg += leadingChar + '"' + servoName + '":' + json.dumps(o.__dict__)
            leadingChar = ','
        jsonMsg += '}'
        config.log(f"getServoCurrentList, leftArm.rotate: {config.servoCurrent['leftArm.rotate'].position}")
        return jsonMsg
    '''

    def exposed_getArduinoData(self):
        jsonizedArduinoData = json.dumps(config.arduinoData)
        return jsonizedArduinoData


    def exposed_requestServoUpdate(self, servoName):
        servoStatic = config.servoStaticDict[servoName]
        servoUpdateData = config.servoCurrentDict[servoName]
        rpcSend.servoUpdate(servoName, servoUpdateData)


    def exposed_requestServoPos(self, servoName, position, duration):
        servoStatic = config.servoStaticDict[servoName]
        config.log(f"request for servo positioning received, servoName: {servoName}, arduino: {servoStatic.arduino}, pin: {servoStatic.pin}, relPos: {position}, duration: {duration}")
        arduinoSend.requestServoPosition(servoName, position, duration)


    def exposed_requestServoDegrees(self, servoName, degrees, duration):
        #config.log(f"request for servo degree received, servoName: {servoName}, degrees: {degrees}, duration: {duration}")
        servoStatic = config.servoStaticDict[servoName]

        if degrees > servoStatic.maxDeg:
            degrees = servoStatic.maxDeg
            config.log(f"{servoName}, requested degrees > max, limited to max {servoStatic.maxDeg}")

        if degrees < servoStatic.minDeg:
            degrees = servoStatic.minDeg
            config.log(f"{servoName}, requested degrees < min, limited to min {servoStatic.maxDeg}")

        position = config.evalPosFromDeg(servoName, degrees)
        #config.log("request position: position")
        arduinoSend.requestServoPosition(servoName, position, duration)


    def exposed_getPosition(self, servoName):
        #config.log(f"get3dPosition received for servo {servoName}", publish=False)
        if servoName in config.servoCurrentDict:
            degrees, position, moving = config.getServoPosition(servoName)
            return degrees, position, moving
        else:
            config.log(f"getPosition-request for unknown servo: {servoName}")
            return None, None, None


    def exposed_requestSetAutoDetach(self, servoName, milliseconds):
        servoStatic = config.servoStaticDict[servoName]
        config.log(f"setAutoDetach received for servo {servoName}, ms: {milliseconds}")
        if servoStatic.autoDetach != milliseconds:
            servoStatic.autoDetach = milliseconds
            arduinoSend.setAutoDetach(servoName, milliseconds)   # update arduino
        return True


    def exposed_requestServoStop(self, servoName):
        config.log(f"requestServoStop received for servo {servoName}")
        arduinoSend.requestServoStop(servoName)
        return True


    def exposed_requestAllServosStop(self):
        arduinoSend.requestAllServosStop()
        config.log(f"requestAllServosStop received")
        return True


    def exposed_requestRest(self, servoName):
        config.log(f"requestSetRest received for servo {servoName}")
        arduinoSend.requestRest(servoName)
        return True


    def exposed_requestRestAll(self):
        config.log(f"requestRestAll received")
        arduinoSend.requestAllServosRest()
        return True


    def exposed_requestSetPosition(self, servoName, newPosition):
        config.log(f"requestSetPosition received for servo {servoName}, pos: {newPosition}")
        arduinoSend.setPosition(servoName, newPosition)
        return True


    def exposed_requestSetVerbose(self, servoName, newState):
        config.log(f"requestSetVerbose received for servo {servoName}, {newState}")
        arduinoSend.setVerbose(servoName, newState)
        return True

    '''
    def exposed_requestSaveServoDict(self, servoName, jsonizedDef):

        newDef = json.loads(jsonizedDef)
        config.servoDict[servoName] = newDef
        config.saveServoDict()
        config.log(f"requestSaveServoDict received for servo {servoName}")

        # update the local store with changed values from servoGui
        servoStatic = config.servoStaticDict[servoName]
        servoStatic.arduino = newDef['arduino']
        servoStatic.servoId = newDef['servoId']
        servoStatic.pin = newDef['pin']
        servoStatic.powerPin = newDef['powerPin']
        servoStatic.minComment = newDef['minComment']
        servoStatic.maxComment = newDef['maxComment']
        servoStatic.minPos = newDef['minPos']
        servoStatic.maxPos = newDef['maxPos']
        servoStatic.zeroDegPos = newDef['zeroDegPos']
        servoStatic.minDeg = newDef['minDeg']
        servoStatic.maxDeg = newDef['maxDeg']
        servoStatic.autoDetach = newDef['autoDetach']
        servoStatic.inverted = newDef['inverted']
        servoStatic.restDeg = newDef['restDeg']
        servoStatic.enabled = newDef['enabled']
        servoStatic.servoType = newDef['servoType']
        servoStatic.cableTerminal = newDef['cableTerminal']
        servoStatic.wireColorArduinoTerminal = newDef['wireColorArduinoTerminal']
        servoStatic.wireColorTerminalServo = newDef['wireColorTerminalServo']

        # update arduino too
        arduinoSend.servoAssign(servoName, servoStatic, config.getPersistedServoPosition(servoName))
    '''

    def exposed_requestMovePose(self):
        config.log(f"requestMovePose received")
        arduinoSend.requestServoPosition('leftHand.thumb', 0, 300)
        arduinoSend.requestServoPosition('leftHand.index', 0, 300)
        arduinoSend.requestServoPosition('leftHand.majeure', 0, 300)
        arduinoSend.requestServoPosition('leftHand.ringFinger', 0, 300)
        arduinoSend.requestServoPosition('leftHand.pinky', 0, 300)
        arduinoSend.requestServoPosition('leftArm.rotate', 65, 300)

        arduinoSend.requestServoPosition('rightHand.thumb', 0, 300)
        arduinoSend.requestServoPosition('rightHand.index', 0, 300)
        arduinoSend.requestServoPosition('rightHand.majeure', 0, 300)
        arduinoSend.requestServoPosition('rightHand.ringFinger', 0, 300)
        arduinoSend.requestServoPosition('rightHand.pinky', 0, 300)
        arduinoSend.requestServoPosition('rightArm.rotate', 65, 300)

        arduinoSend.requestServoDegrees('head.neck', 0, 300)
        arduinoSend.requestServoDegrees('head.rothead', 0, 300)


    def exposed_pinHigh(self, pinList):
        pList = list(pinList)
        config.log(f"pinHigh to arduino: {pList}")
        arduinoSend.pinHigh(pList)


    def exposed_pinLow(self, pinList):
        pList = list(pinList)
        config.log(f"pinLow to arduino: {pList}")
        arduinoSend.pinLow(pList)


    def exposed_setServosSimulated(self, newState):
        config.log(f"servo simulation state changed, simulateServoMoves: {newState}")
        config.simulateServoMoves = newState


    def exposed_setAutoDetach(self, servoName, durationMs):
        config.log(f"set auto detach for servo {servoName} to {durationMs} Ms")
        servoStatic = config.servoStaticDict[servoName]
        arduinoSend.setAutoDetach(servoStatic, durationMs)