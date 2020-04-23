
import time

import config
import simplejson as json

import rpcReceive


def servoUpdate(servoName, servoUpdateData):

    msg = json.dumps(servoUpdateData.__dict__)
    for c in config.clientList:

        if c['replyConn'] is None:
            config.log(f"ERROR: no reply connection with client {c['clientId']} yet")
            config.log(f"connections: {config.clientList}")

        else:
            if c['messageList'] == [] or 'servoUpdate' in c['messageList']:

                try:
                    c['replyConn'].root.servoUpdate(servoName, msg)

                except TimeoutError as t:
                    config.log(f"ignoring rpc timeout error in servoUpdate")

                except Exception as e:
                    print(f"exception in publishServoUpdate: {str(e)}")
                    c['replyConn'] = None

    if config.verbose:
        config.log(f"servoUpdate published, {servoName}, {msg}", publish=False)


def publishArduinoState(arduino, state: bool):

    # inform all clients about the update
    for i, c in enumerate(config.clientList):

        if c['replyConn'] is not None:
            if c['messageList'] == [] or 'publishArduinoState' in c['messageList']:

                try:
                    c['replyConn'].root.exposed_arduinoUpdate

                except Exception as e:
                    print(f"arduinoUpdate is not implemented on client: {str(e)}")
                    return

                try:
                    c.root.arduinoUpdate(arduino, state)

                except Exception as e:
                    print(f"exception in publishArduinoState: {str(e)}")


def publishLog(msg):

    for i, c in enumerate(config.clientList):
        if c['replyConn'] is not None:
            if c['messageList'] == [] or 'publishLog' in c['messageList']:
                try:
                    c['replyConn'].root.exposed_log(msg)

                except TimeoutError as t:
                    config.log(f"ignoring rpc timeout error in log")

                except Exception as e:
                    print(f"exception in publishLog to client {c['clientId']}, : {e}")
                    c['replyConn'] = None


def publishLifeSignal():

    #config.log(f"publishing life signal")
    for c in config.clientList:
        if c['replyConn'] is not None:
            try:
                c['replyConn'].root.exposed_lifeSignalUpdate(config.serverName)
                #config.log(f"published life signal to {c['clientId']} ", publish = False)

            #except TimeoutError as t:
            #    config.log(f"ignoring rpc timeout error in lifeSignalUpdate")

            except Exception as e:
                c['replyConn'] = None
                config.log(f"exception in publishLifeSignal with {c['clientId']}: {e}")


def publishBasicData():

    config.log(f"publishing basic servo data message to clients")

    # build a json message with static data of all servos
    jsonMsg = ''
    leadingChar = '{'
    for servoName in config.servoStaticDict:  # objectviews of the servoDefinitions (dict attribs accessible with . notation)
        jsonMsg += leadingChar + '"' + servoName + '":' + json.dumps(config.servoStaticDict[servoName].__dict__)
        leadingChar = ','
    jsonMsg += '}'

    for i, c in enumerate(config.clientList):

        if c['replyConn'] is not None:
            if c['messageList'] == [] or 'publishBasicData' in c['messageList']:
                try:
                    c['replyConn'].root.exposed_robotControlBasicData(jsonMsg)

                except TimeoutError as t:
                    config.log(f"ignoring rpc timeout error in sending basic data")

                except Exception as e:
                    c['replyConn'] = None
                    config.log(f"exception in publishBasicData to {c['clientId']}: {e}")


def publishServerReady():

    config.log(f"publishing ready={config.serverReady} message to clients")

    for i, c in enumerate(config.clientList):

        if c['replyConn'] is not None:
            if c['messageList'] == [] or 'publishServerReady' in c['messageList']:
                try:
                    c['replyConn'].root.exposed_serverReady(config.serverName, config.serverReady)

                except TimeoutError as t:
                    config.log(f"ignoring rpc timeout error in serverReady")

                except Exception as e:
                    c['replyConn'] = None
                    config.log(f"exception in publishServerReady with {c['clientId']}: {e}")

