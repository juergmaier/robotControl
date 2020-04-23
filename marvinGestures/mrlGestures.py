

handServos = ['Hand.thumb',
              'Hand.index',
              'Hand.majeure',
              'Hand.ringFinger',
              'Hand.pinky',
              'Hand.wrist']
handMoveDuration = {
    'leftHand.thumb' : {'default': 500, 'current': 500},
    'leftHand.index' : {'default': 500, 'current': 500},
    'leftHand.majeure' : {'default': 500, 'current': 500},
    'leftHand.ringFinger' : {'default': 500, 'current': 500},
    'leftHand.pinky' : {'default': 500, 'current': 500},
    'leftHand.wrist' : {'default': 500, 'current': 500},
    'rightHand.thumb' : {'default': 500, 'current': 500},
    'rightHand.index' : {'default': 500, 'current': 500},
    'rightHand.majeure' : {'default': 500, 'current': 500},
    'rightHand.ringFinger' : {'default': 500, 'current': 500},
    'rightHand.pinky' : {'default': 500, 'current': 500},
    'rightHand.wrist' : {'default': 500, 'current': 500}
}

armServos = ['Arm.bicep',
             'Arm.rotate',
             'Arm.shoulder',
             'Arm.omoplate']
armMoveDuration = {
    'leftArm.bicep' : {'default': 800, 'current': 800},
    'rightArm.bicep' : {'default': 800, 'current': 800},
    'leftArm.rotate' : {'default': 800, 'current': 800},
    'rightArm.rotate' : {'default': 800, 'current': 800},
    'leftArm.shoulder' : {'default': 800, 'current': 800},
    'rightArm.shoulder' : {'default': 800, 'current': 800},
    'leftArm.omoplate' : {'default': 800, 'current': 800},
    'rightArm.omoplate' : {'default': 800, 'current': 800} }


headServos = ['head.rothead',
              'head.neck']
headMoveDuration =  {'head.rothead' : {'default': 800, 'current': 800},
                     'head.neck': {'default': 800, 'current': 800}}

eyeServos = ['head.eyeX',
             'head.eyeY']
eyeMoveDuration =  {'head.eyeX' : {'default': 800, 'current': 800},
                    'head.eyeY': {'default': 800, 'current': 800}}

torsservoStatics = ['torso.topStom',
               'torso.midStom'
               'torso.lowStom']
torsoMoveDuration =  {'torso.topStom' : {'default': 800, 'current': 800},
                      'torso.midStom' : {'default': 800, 'current': 800},
                      'torso.lowStom' : {'default': 800, 'current': 800}}


gestureDir = 'c:/projekte/inmoov/robotControl/marvinGestures'   # change this to marvinGestures once all gestures are verified


def createAllGesturesModule():

    with open('allGestures.py','w') as wfd:

        wfd.writelines("from mrlGestures import *\n")
        wfd.writelines("import i01\n")
        wfd.writelines("import ear\n")
        wfd.writelines("\n")
        wfd.writelines("isNeopixelActivated = False\n")
        wfd.writelines("\n")

        for item in os.listdir(gestureDir):
            file = gestureDir + "/" + item
            config.log(f"adding file to allGestures: {item}")
            with open(file,'r') as fd:
                shutil.copyfileobj(fd, wfd)
                wfd.writelines("\n")
                wfd.writelines("\n")

    importlib.reload(allGestures)



def runSelectGesture(gestureName):
    gestureName()


def setHandSpeed(side, thumbSpeed, indexSpeed, majeureSpeed, ringFingerSpeed, pinkySpeed, wristSpeed):
    global handMoveDuration
    handMoveDuration[side + 'Hand.thumb']['current'] = handMoveDuration[side + 'Hand.thumb']['default'] / float(thumbSpeed)
    handMoveDuration[side + 'Hand.index']['current'] = handMoveDuration[side + 'Hand.index']['default'] / float(indexSpeed)
    handMoveDuration[side + 'Hand.majeure']['current'] = handMoveDuration[side + 'Hand.majeure']['default'] / float(majeureSpeed)
    handMoveDuration[side + 'Hand.ringFinger']['current'] = handMoveDuration[side + 'Hand.ringFinger']['default'] / float(ringFingerSpeed)
    handMoveDuration[side + 'Hand.pinky']['current'] = handMoveDuration[side + 'Hand.pinky']['default'] / float(pinkySpeed)
    handMoveDuration[side + 'Hand.wrist']['current'] = handMoveDuration[side + 'Hand.wrist']['default'] / float(wristSpeed)


def setArmSpeed(side, bicepSpeed, shoulderSpeed, rotateSpeed, omoplateSpeed):
    global armMoveDuration
    config.log(f"setArmSpeed {side}, {bicepSpeed}, {shoulderSpeed}, {rotateSpeed}, {omoplateSpeed}")
    armMoveDuration[side + 'Arm.bicep']['current'] = armMoveDuration[side + 'Arm.bicep']['default'] / float(bicepSpeed)
    armMoveDuration[side + 'Arm.rotate']['current'] = armMoveDuration[side + 'Arm.rotate']['default'] / float(rotateSpeed)
    armMoveDuration[side + 'Arm.shoulder']['current'] = armMoveDuration[side + 'Arm.shoulder']['default'] / float(shoulderSpeed)
    armMoveDuration[side + 'Arm.omoplate']['current'] = armMoveDuration[side + 'Arm.omoplate']['default'] / float(omoplateSpeed)


def setHeadSpeed(rotHeadSpeed, neckSpeed):
    global headMoveDuration
    headMoveDuration['head.rothead']['current'] = headMoveDuration['head.rothead']['default'] / float(rotHeadSpeed)
    headMoveDuration['head.neck']['current'] = headMoveDuration['head.neck']['default'] / float(neckSpeed)


def setTorsoSpeed(topStomSpeed, midStomSpeed, lowStomSpeed=800):
    global torsoMoveDuration
    torsoMoveDuration['torso.topStom']['current'] = torsoMoveDuration['torso.topStom']['default'] / float(topStomSpeed)
    torsoMoveDuration['torso.midStom']['current'] = torsoMoveDuration['torso.midStom']['default'] / float(midStomSpeed)

def setEyeSpeed(eyeXSpeed, eyeYSpeed):
    global eyeMoveDuration
    eyeMoveDuration['head.eyeX']['current'] = torsoMoveDuration['head.eyeX']['default'] / float(eyeXSpeed)
    eyeMoveDuration['head.eyeY']['current'] = torsoMoveDuration['head.eyeY']['default'] / float(eyeXSpeed)


def sleep(seconds=0):
    time.sleep(seconds)

def rest():
    i01.rest()

def relax():
    i01.rest()
