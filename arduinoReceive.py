
import os
import sys
import time

import config
import rpcSend
import arduinoSend
import ik


#####################################
# readMessages runs in its own THREAD
#####################################
def readMessages(arduino):

    config.log(f"arduinoReceive, readMessages started for arduino: {arduino}")

    while True:
        if config.arduinoConn[arduino] is None:
            time.sleep(1)
            continue

        conn = config.arduinoConn[arduino]
        if conn.is_open:

            try:
                bytesAvailable = conn.in_waiting
            except Exception as e:
                config.log(f"exception in arduino: {arduino} in in_waiting {e}, shutting down ...")
                os._exit(1)

            if bytesAvailable > 0:

                recvB = conn.readline()

                # special case status messages, as these can be very frequently
                # a compressed format is used
                if recvB[0] & 0x80 == 0x80:

                    if len(recvB) != 4:     # including cr!
                        config.log("received corrupt status message from arduino, len != 3")
                        continue

                    # extract data from binary message
                    pin =        recvB[0] & 0x7f
                    position =   recvB[1] -40           # to prevent value seen as lf 40 is added by the arduino
                    assigned =   recvB[2] & 0x01 > 0
                    moving =     recvB[2] & 0x02 > 0
                    attached =   recvB[2] & 0x04 > 0
                    autoDetach = recvB[2] & 0x08 > 0
                    servoVerbose =    recvB[2] & 0x10 > 0

                    servoUniqueId = (arduino * 100) + pin
                    servoName = config.servoNameByArduinoAndPin[servoUniqueId]

                    if servoVerbose:
                        config.log(f"servo update, {recvB[0]:02X},{recvB[1]:02X},{recvB[2]:02X}, arduino: {arduino}, pin: {pin:2}, servo: {servoName}, pos {position:3}, assigned: {assigned}, moving {moving}, attached {attached}, autoDetach: {autoDetach}, verbose: {servoVerbose}", publish=False)

                    degrees = config.evalDegFromPos(servoName, position)
                    #config.log(f'arduino, servoName: {servoName}, moving: {moving}')
                    prevPosition = config.servoCurrentDict[servoName].position

                    #if servoName == 'leftArm.rotate':
                    #    config.log(f"leftArm.rotate new position: {position}")

                    config.servoCurrentDict[servoName].updateData(degrees, position, assigned, moving, attached, autoDetach, servoVerbose)
                    # update the shared dict too
                    if config.marvinShares is not None:
                        config.marvinShares.updateServoCurrentDict(servoName, config.servoCurrentDict[servoName])

                    if position != prevPosition:
                        ik.updateDhChain()

                    # check for move target postition reached
                    if not moving and attached:

                        # persist last position of servo
                        config.saveServoPosition(servoName, position)
                        if config.verbose:
                            config.log(f"move stopped, servo: {servoName}, position: {position}, degrees: {degrees}")

                        # handle special case in swipe mode
                        if config.swipingServoName is not None:
                            if config.nextSwipePos == config.servoStaticDict[config.swipingServoName].minPos:
                                config.nextSwipePos = config.servoStaticDict[config.swipingServoName].maxPos
                            else:
                                config.nextSwipePos = config.servoStaticDict[config.swipingServoName].minPos
                            arduinoSend.requestServoPosition(config.swipingServoName, config.nextSwipePos, config.SWIPE_MOVE_DURATION)

                    # update gui
                    servoUpdateData = config.servoCurrentDict[servoName]
                    ###################################################
                    # ATTENTION: not using copy modifies servoCurrent
                    # with many side effects
                    ###################################################
                    guiData = servoUpdateData.__dict__.copy()
                    guiData.update({'type': config.SERVO_UPDATE})
                    #config.log(f"guiData with type: {guiData}")
                    config.guiUpdateQueue.put(guiData)

                    # publish servo update messages only after a connection to a client has been established
                    if config.serverReady:

                        # inform interrested clients about the update
                        rpcSend.servoUpdate(servoName, servoUpdateData)

                    continue


                # now process all other messages not starting with 0x80 byte
                try:
                    recv = recvB.decode()
                except:
                    config.log(f"problem with decoding arduino msg '{recvB}'")
                    continue

                # config.log(f"line read {recv}")
                msgID = recvB[0:3].decode()


                if msgID == "!A0":  # "arduino ready"

                    config.arduinoData[arduino]['connected'] = True

                    info = {'type': config.ARDUINO_UPDATE, 'arduino': arduino, 'connected': True}
                    config.guiUpdateQueue.put(info)

                    #rpcSend.publishArduinoState(arduino, True)
                    #config.log("arduino status update sent to client")

                else:
                    try:
                        config.log(f"<-I{arduino} " + recv[:-1], publish=False)
                    except:
                        config.log(f"Unexpected error on reading messages: {sys.exc_info()[0]}")

        time.sleep(0.01)  # give other threads a chance
