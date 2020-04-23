
import time

import config
import rpcSend
import inmoovGlobal

# monitor the network connections

def watchDog():

    while True:

        # watchdog for incoming commands from clients
        # remove client if we do not get regular messages
        for i, c in enumerate(config.clientList):

            timeSinceLastMessage = time.time() - c['lifeSignalReceived']

            if timeSinceLastMessage > inmoovGlobal.RPYC_HEARTBEAT_INTERVAL * 1.5:

                config.log(f"no message from {c['clientId']} for {timeSinceLastMessage:.1f} s")
                config.log(f"remove client: {c['clientId']} from client list")
                del config.clientList[i]

        # send life signal to clients
        rpcSend.publishLifeSignal()

        time.sleep(inmoovGlobal.RPYC_HEARTBEAT_INTERVAL)

