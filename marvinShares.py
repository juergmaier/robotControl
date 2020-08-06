
import sys

# from examples
from multiprocessing.managers import SyncManager
from multiprocessing import Process, Queue, Manager

import config


class ShareManager(SyncManager): pass

class MarvinShares(Process):
    "shared ressources in its own process"
    def __init__(self):
        super().__init__()

        # locally and remote accessible queues
        self.speechRequests = Queue();
        self.speechResponds = Queue();

        self.servoRequests = Queue();

        # shared dictionaries
        shareManager = Manager()
        self.servoStaticDict = shareManager.dict()
        for key in config.servoStaticDict:
            self.servoStaticDict[key] = config.servoStaticDict[key]

        self.servoCurrentDict = shareManager.dict()

    def updateServoStaticDict(self, servoName, servoStatic):
        self.servoStaticDict[servoName] = servoStatic

    def getServoStaticDict(self):
        return self.servoStaticDict

    def updateServoCurrentDict(self, servoName, servoCurrent):
        self.servoCurrentDict[servoName] = servoCurrent

    def getServoCurrentDict(self):
        return self.servoCurrentDict


    def run(self):
        # create the shared queues
        ShareManager.register('getSpeechRequestQueue', callable=lambda:self.speechRequests)
        ShareManager.register('getSpeechRespondQueue', callable=lambda:self.speechResponds)
        ShareManager.register('getServoRequestQueue', callable=lambda:self.servoRequests)

        ShareManager.register('getServoStaticDict', self.getServoStaticDict)
        ShareManager.register('getServoCurrentDict', self.getServoCurrentDict)

        try:
            m = ShareManager(address=('', 50002), authkey=b'marvin')
            config.log(f"marvinShares: shareManager instanciated")
            s = m.get_server()
            config.log(f"marvinShares: registered, start serve_forever")
            s.serve_forever()

        except Exception as e:
            config.log(f"marvin shares problem, {e}")




