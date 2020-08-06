

import config
import arduinoSend



def processServoRequests():
    """
    servo request is a dict with at least a request field
    :arg
    """
    def requestDegrees():
        try:
            servoName = msg['servoName']
            degrees = msg['degrees']
            duration = msg['duration']
            if 'filterSequence' in msg:
                filterSequence = msg['filterSequence']
            else:
                filterSequence = True

        except KeyError:
            config.log(f"servo request with wrong structure {msg}")
            return

        position = config.evalPosFromDeg(servoName, degrees)
        arduinoSend.requestServoPosition(servoName, position, duration, filterSequence)


    def requestPosition():
        try:
            servoName = msg['servoName']
            position = msg['position']
            duration = msg['duration']
            if 'filterSequence' in msg:
                filterSequence = msg['filterSequence']
            else:
                filterSequence = True

        except KeyError:
            config.log(f"servo request with wrong structure {msg}")
            return

        arduinoSend.requestServoDegrees(servoName, position, duration, filterSequence)


    def requestSetAutoDetach():
        try:
            servoName = msg['servoName']
            milliseconds = msg['milliseconds']

        except KeyError:
            config.log(f"servo request with wrong structure {msg}")
            return

        arduinoSend.setAutoDetach(servoName, milliseconds)


    def requestServoStop():
        try:
            servoName = msg['servoName']

        except KeyError:
            config.log(f"servo request with wrong structure {msg}")
            return

        arduinoSend.requestServoStop(servoName)


    def requestAllServoStop():
        arduinoSend.requestAllServosStop()


    def requestRest():
        try:
            servoName = msg['servoName']

        except KeyError:
            config.log(f"servo request with wrong structure: {msg}")
            return

        arduinoSend.requestRest(servoName)


    def requestRestAll():
        arduinoSend.requestAllServosRest()


    switcher = {
        'degrees':      requestDegrees,
        'position':     requestPosition,
        'setAutoDetach': requestSetAutoDetach,
        'servoStop':    requestServoStop,
        'allServoStop': requestAllServoStop,
        'rest':         requestRest,
        'restAll':      requestRestAll
    }


    while True:

        # wait for incoming messages
        msg = config.marvinShares.servoRequests.get()

        config.log(f"servo request received: {msg}")

        if type(msg) is not dict:
            config.log(f"a servo request has to be a dict")

        if 'request' not in msg:
            config.log(f"a servo request dict has to contain the key 'request'")

        func = switcher.get(msg['request'], None)

        if func is None:
            config.log(f"unknown servo request: {msg}")
        else:
            func()
