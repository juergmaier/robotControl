# 2016-02-12 juerg maier
# Use Danevit Hartenberg parameters to calculate current x,y,z Position of Palm

from copy import deepcopy
import numpy as np
import time

import config


#REVOLUTE = 0
#LINEAR = 1      # also called prismatic


# first joint is Z rotation (fixed values for InMoov cart Z rotation)
T = [[ 1.0, 0.0, 0.0, 0.0],
     [ 0.0, 1.0, 0.0, 0.0],
     [ 0.0, 0.0, 1.0, 0.0],
     [ 0.0, 0.0, 0.0, 1.0]]

dhKeys = ["servoName","jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]


# dh parameters <joint offset | d>, <theta | joint angle>, <link length | a | r>, <twist angle | alpha>
# also referenced as d, theta, r or a, alpha

dhRightArm = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['cartYaw',            0.0  ,     0.0,       0.05 ,     0.0,           1,           1],
    ['tableHeight',        0.9  ,     0.0,       0.0  ,     0.0,           1,           1],
    ['torso.midStom',      0.0  ,   -90.0,       0.0  ,     0.0,           1,           1],
    ['torso.topStom',      0.11 ,    90.0,       0.0  ,    90.0,           1,           8],
    ['none',               0.0  ,    65.0,       0.325,     0.0,           1,           1], # link to shoulder right
    ['rightArm.omoplate',  0.0  ,    25.0,      -0.05 ,    90.0,           1,           1],
    ['rightArm.shoulder',  0.08 ,   -90.0,       0.0  ,    90.0,           1,           1],
    ['rightArm.rotate',    0.0  ,     0.0,       0.0  ,    90.0,           1,           1],
    ['none',               0.0  ,     0.0,       0.0  ,   -90.0,           1,           1],
    ['none',               0.28 ,     0.0,       0.0  ,    90.0,           1,           5],
    ['rightArm.bicep',     0.0  ,   180.0,       0.0  ,    90.0,          -1,           1],
    ['rightHand.wrist',    0.3  ,     0.0,       0.0  ,     0.0,           1,           5],
]

dhRightPinky = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,          1,           1],    # axis change for finger root link
    ['none',               0.0  ,    65.0,       0.117,     0.0,           0,           1],    # fixed link to finger root
    ['none',               0.0  ,    25.0,       0.0  ,    90.0,           1,           1],    # dummy for angle and axis change
    ['rightHand.pinky',    0.0  ,     0.0,       0.03 ,     0.0,          -1,           2],    # proximal
    ['rightHand.pinky',    0.0  ,     0.0,       0.02 ,     0.0,          -1,           2],    # middle
    ['rightHand.pinky',    0.0  ,     0.0,       0.025,     0.0,          -1,           2],    # distal
]

dhRightRing = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,          0,           1],    # axis change for finger root link
    ['none',               0.0  ,    78.0,       0.12 ,     0.0,           0,           1],    # fixed link to finger root
    ['none',               0.0  ,    12.0,       0.0  ,    90.0,           0,           1],    # dummy for angle and axis change
    ['rightHand.ringFinger',0.0  ,    0.0,       0.04 ,     0.0,          -1,           2],    # proximal
    ['rightHand.ringFinger',0.0  ,    0.0,       0.025,     0.0,          -1,           2],    # middle
    ['rightHand.ringFinger',0.0  ,    0.0,       0.03 ,     0.0,          -1,           2],    # distal
]

dhRightMiddle = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,          0,           1],    # axis change for finger root link
    ['none',               0.0  ,    95.0,        0.15 ,     0.0,          0,           1],    # fixed link to finger root
    ['none',               0.0  ,    -5.0,        0.0  ,    90.0,          0,           1],    # dummy for angle and axis change
    ['rightHand.majeure',  0.0  ,     0.0,        0.035,     0.0,         -1,           2],    # proximal
    ['rightHand.majeure',  0.0  ,     0.0,        0.025,     0.0,         -1,           2],    # middle
    ['rightHand.majeure',  0.0  ,     0.0,        0.035,     0.0,         -1,           2],    # distal
]

dhRightIndex = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,          1,           1],    # axis change for finger root link
    ['none',               0.0  ,   109.0,        0.13 ,     0.0,          1,           1],    # fixed link to finger root
    ['none',               0.0  ,   -19.0,        0.0  ,   -90.0,          1,           1],    # finger parts rotations axis
    ['rightHand.index',    0.0  ,     0.0,        0.035,     0.0,          1,           2],    # proximal
    ['rightHand.index',    0.0  ,     0.0,        0.025,     0.0,          1,           2],    # middle
    ['rightHand.index',    0.0  ,     0.0,        0.030,     0.0,          1,           2],    # distal
]

dhRightThumb = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,       0.0  ,    90.0,           1,           1],    # axis change for finger root link
    ['none',               0.0  ,   117.0,       0.065,     0.0,           1,           1],    # fixed link to thumb base
    ['none',               0.0  ,  -117.0,       0.0  ,    90.0,           1,           1],    # get parallel to wrist again
    ['rightHand.thumb',    0.0  ,   180.0,       0.03 ,    90.0,           1,           2],    # first joint
    ['none',               0.0  ,   -60.0,       0.0  ,    90.0,           1,           1],    # fixed link to second joint
    ['rightHand.thumb',    0.0  ,     0.0,       0.033,     0.0,          -1,           2],    # middle
    ['rightHand.thumb',    0.0  ,     0.0,       0.033,     0.0,          -1,           2],    # distal
]


dhLeftArm = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['cartYaw',            0.0  ,     0.0,       0.05 ,     0.0,           1,           1],
    ['tableHeight',        0.9  ,    90.0,       0.0  ,     0.0,           1,           1],
    ['torso.midStom',      0.0  ,   -90.0,       0.0  ,     0.0,           1,           1],
    ['torso.topStom',      0.11 ,    90.0,       0.0  ,    90.0,           1,           1],
    ['none',               0.0  ,   115.0,       0.325,     0.0,           1,           1], # fixed link to shoulder left
    ['leftArm.omoplate',   0.0  ,   -25.0,      -0.05 ,    90.0,          -1,           1],
    ['leftArm.shoulder',  -0.08 ,   -90.0,       0.0  ,    90.0,           1,           1],
    ['leftArm.rotate',     0.0  ,     0.0,       0.0  ,    90.0,           1,           1],
    ['none',               0.0  ,     0.0,       0.0  ,   -90.0,           1,           1],
    ['none',               0.28 ,     0.0,       0.0  ,    90.0,           1,           5],
    ['leftArm.bicep',      0.0  ,   180.0,       0.0  ,    90.0,          -1,           1],
    ['leftHand.wrist',     0.3  ,     0.0,       0.0  ,     0.0,           1,           5],
]

dhLeftPinky = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,       0.0  ,    90.0,           1,           1],    # wrist base
    ['none',               0.0  ,    65.0,       0.117,     0.0,           1,           2],    # fixed link to finger root
    ['none',               0.0  ,    25.0,       0.0  ,    90.0,           1,           2],    # back to finger bend rotation axis
    ['leftHand.pinky',     0.0  ,     0.0,       0.03 ,     0.0,           1,           2],    # proximal
    ['leftHand.pinky',     0.0  ,     0.0,       0.02 ,     0.0,           1,           2],    # middle
    ['leftHand.pinky',     0.0  ,     0.0,       0.025,     0.0,           1,           2],    # distal
]

dhLeftRing = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,       0.0  ,    90.0,           1,           1],    # fixed link to finger root
    ['none',               0.0  ,    78.0,       0.12 ,     0.0,           1,           1],    # dummy for angle and axis change
    ['none',               0.0  ,    12.0,       0.0  ,    90.0,           1,           1],    # back to finger bend rotation axis
    ['leftHand.ringFinger',0.0  ,     0.0,       0.04 ,     0.0,           1,           2],    # proximal
    ['leftHand.ringFinger',0.0  ,     0.0,       0.025,     0.0,           1,           2],    # middle
    ['leftHand.ringFinger',0.0  ,     0.0,       0.03 ,     0.0,           1,           2],    # distal
]

dhLeftMiddle = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,       0.0  ,    90.0,           1,           1],    # fixed link to finger root
    ['none',               0.0  ,    95.0,       0.12 ,     0.0,           1,           1],    # dummy for angle and axis change
    ['none',               0.0  ,    -5.0,       0.0  ,    90.0,           1,           1],    # back to finger bend rotation axis
    ['leftHand.majeure',   0.0  ,     0.0,       0.035,     0.0,           1,           2],    # proximal
    ['leftHand.majeure',   0.0  ,     0.0,       0.025,     0.0,           1,           2],    # middle
    ['leftHand.majeure',   0.0  ,     0.0,       0.035,     0.0,           1,           2],    # distal
]

dhLeftIndex = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,          1,          1],    # axis change for finger root link
    ['none',               0.0  ,   109.0,        0.12 ,     0.0,          1,          1],    # link from wrist to finger root
    ['none',               0.0  ,   -19.0,        0.0  ,    90.0,          1,          1],    # rotation axis finger parts
    ['leftHand.index',     0.0  ,     0.0,        0.035,     0.0,          1,          2],    # proximal
    ['leftHand.index',     0.0  ,     0.0,        0.025,     0.0,          1,          2],    # middle
    ['leftHand.index',     0.0  ,     0.0,        0.030,     0.0,          1,          2],    # distal
]

#dhLeftThumb = [
#    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
#    ['none',               0.02 ,     0.0,        0.0  ,    90.0,           1,         1],    # axes change from wrist rotation to hand left/right
#    ['none',               0.0  ,   125.0,        0.035,    90.0,           1,         1],    # angle to thumb base
#    ['leftHand.thumb',     0.0  ,    90.0,        0.035,     0.0,          -1,         1],    # from proximal axis to middle axis
#    ['leftHand.thumb',     0.0  ,    90.0,        0.04 ,     0.0,          -1,         1],    # length and axis change for middle
#    ['leftHand.thumb',     0.0  ,    90.0,        0.035,     0.0,          -1,         1],    # length of distal
#]
dhLeftThumb = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',               0.0  ,     0.0,        0.0  ,    90.0,           1,         1],    # axes change from wrist rotation to hand left/right
    ['none',               0.0  ,    63.0,        0.065,     0.0,           1,         1],    # fixed link to thumb base
    ['none',               0.0  ,   -63.0,        0.0  ,    90.0,           1,         1],    # get parallel to wrist again
    ['leftHand.thumb',     0.0  ,     0.0,        0.03 ,    90.0,           1,         2],    # the base joint of the thumb
    ['none',               0.0  ,   -60.0,        0.0  ,    90.0,           1,         1],    # fixed link to second joint
    ['leftHand.thumb',     0.0  ,     0.0,        0.033,     0.0,          -1,         2],    # middle
    ['leftHand.thumb',     0.0  ,     0.0,        0.033,     0.0,          -1,         2],    # distal
]


dhHead = [
    #["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['cartYaw',            0.0  ,     0.0,        0.05 ,     0.0,           1,          1],
    ['tableHeight',        0.9  ,     0.0,        0.0  ,     0.0,           1,          1],
    ['torso.midStom',      0.0  ,   -90.0,        0.0  ,     0.0,           1,          1],
    ['torso.topStom',      0.11 ,    90.0,        0.0  ,     0.0,           1,          1],
    ['none',               0.44 ,    90.0,        0.0  ,    90.0,           1,          1],    # connection to neck
    ['head.neck',          0.0  ,    0.0,        0.0,    -90.0,           1,          1],
    #['none',               0.0  ,    0.0,        0.0 ,    0.0,           1,          1],
    ['head.rothead',       0.04 ,    0.0,        0.0  ,    0.0,           1,          2]
]

dhLeftEye = [
    # ["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',                0.07 ,    13.0,        0.13 ,     0.0,          1,          1],
    ['head.eyeX',           0.0  ,   -13.0,        0.0  ,    90.0,          1,          1],
    ['head.eyeY',           0.0  ,     0.0,        0.01 ,     0.0,          1,          4]
]

dhRightEye = [
    # ["servoName", "jointOffset", "theta", "linkLength", "alpha", "thetaMul", "linewidth"]
    ['none',                0.07 ,   -13.0,        0.13 ,     0.0,          1,          1],
    ['head.eyeX',           0.0  ,    13.0,        0.0  ,    90.0,          1,          1],
    ['head.eyeY',           0.0  ,     0.0,        0.01 ,     0.0,          1,          4]
]

# 'chain' gets set in initialization
dhChains = {
    'rightArm':         {'chain': None, 'dhParams': dhRightArm,   'prevChain': None},
    'rightHand.pinky':  {'chain': None, 'dhParams': dhRightPinky, 'prevChain': 'rightArm'},
    'rightHand.ring':   {'chain': None, 'dhParams': dhRightRing,  'prevChain': 'rightArm'},
    'rightHand.middle': {'chain': None, 'dhParams': dhRightMiddle,'prevChain': 'rightArm'},
    'rightHand.thumb':  {'chain': None, 'dhParams': dhRightThumb, 'prevChain': 'rightArm'},
    'rightHand.index':  {'chain': None, 'dhParams': dhRightIndex, 'prevChain': 'rightArm'},
    'leftArm':          {'chain': None, 'dhParams': dhLeftArm,    'prevChain': None},
    'leftHand.pinky':   {'chain': None, 'dhParams': dhLeftPinky,  'prevChain': 'leftArm'},
    'leftHand.ring':    {'chain': None, 'dhParams': dhLeftRing,   'prevChain': 'leftArm'},
    'leftHand.middle':  {'chain': None, 'dhParams': dhLeftMiddle, 'prevChain': 'leftArm'},
    'leftHand.index':   {'chain': None, 'dhParams': dhLeftIndex,  'prevChain': 'leftArm'},
    'leftHand.thumb':   {'chain': None, 'dhParams': dhLeftThumb,  'prevChain': 'leftArm'},
    'head':             {'chain': None, 'dhParams': dhHead,       'prevChain': None},
    'leftEye':          {'chain': None, 'dhParams': dhLeftEye,    'prevChain': 'head'},
    'rightEye':         {'chain': None, 'dhParams': dhRightEye,   'prevChain': 'head'}
}



#out = np.zeros((500,500,3), dtype=np.uint8)
prevPoint = None


class cJoint:
    def __init__(self, jointDefinition):
        self.servoName =    jointDefinition['servoName']
        self.jointOffset =  jointDefinition['jointOffset']
        self.theta =        jointDefinition['theta']
        self.linkLength =   jointDefinition['linkLength']
        self.alpha =        jointDefinition['alpha']
        self.thetaMul =     jointDefinition['thetaMul']
        self.linewidth =    jointDefinition['linewidth']
        self.positionX =    0
        self.positionY =    0
        self.positionZ =    0
        self.positionChanged =   False

    def updatePosition(self, x, y, z):
        if x != self.positionX or y != self.positionY or z != self.positionZ:
            self.positionChanged = True
        self.positionX = x
        self.positionY = y
        self.positionZ = z

    def getPositionChanged(self): return self.positionChanged

    def get3dPosition(self):
        return (self.positionX, self.positionY, self.positionZ)

    def get3dPositionAndSize(self):
        return (self.positionX, self.positionY, self.positionZ, self.linewidth)


class cJointChain:

    def __init__(self, params):
        self.joints = []
        self.endEffector = None
        self.prevChain = None
        self.loadParameters(params)

    def loadParameters(self, params):

        for dhDef in params:
            dhDict = dict(zip(dhKeys,dhDef))    # store as dict to access values by name
            self.addJoint(cJoint(dhDict))

    def addJoint(self, joint):
        self.joints.append(joint)


    def getEndEffector(self):
        return self.endEffector


    def dhCalc(self, prevChain=None):

        if prevChain is None:
            self.endEffector = deepcopy(T)	# initial identity matrix
        else:
            # use end effector of prev chain
            self.prevChain = dhChains[prevChain]['chain']
            try:
                self.endEffector = dhChains[prevChain]['chain'].getEndEffector()
            except Exception as e:
                config.log(f"exception in dhCalc getting end effector, {e}")

        #######################################
        # walk through all the joints
        #######################################
        for j in self.joints:

            # handle special joints
            if j.servoName == 'cartYaw':
                servoTheta = 90
            elif j.servoName == 'tableHeight':
                servoTheta = -90
            elif j.servoName == 'none':
                servoTheta = j.theta
            else:
                servoTheta = config.servoCurrentDict[j.servoName].degrees * j.thetaMul + j.theta

            ct = np.cos(np.radians(servoTheta))  #cosinus(theta)
            st = np.sin(np.radians(servoTheta))  #sinus(theta)
            ca = np.cos(np.radians(j.alpha))  #cosinus(alpha)
            sa = np.sin(np.radians(j.alpha))  #sinus(alpha)

            # set the matrix values according to the dh-parameters
            t1 = np.array([
                [   ct, -st*ca,  st*sa,  ct*j.linkLength],
                [   st,  ct*ca, -ct*sa,  st*j.linkLength],
                [  0.0,     sa,     ca,     j.jointOffset],
                [  0.0,    0.0,    0.0,               1.0] ])

            #print(f"endEffector: {self.endEffector}")
            self.endEffector = np.matmul(self.endEffector, t1)
            j.updatePosition(self.endEffector[0][3], self.endEffector[1][3], self.endEffector[2][3])


    def positions(self):
        data = [(0,0,0,1)]      # base point
        if self.prevChain is not None:
            data = [self.getLastPositionAndSize(self.prevChain)]
        for j in self.joints:
            data.append(j.get3dPositionAndSize())
        return data


    def getLastPosition(self, chain):
        lastJoint = chain.joints[-1]
        return lastJoint.get3dPosition()


    def getLastPositionAndSize(self, chain):
        lastJoint = chain.joints[-1]
        return lastJoint.get3dPositionAndSize()

#################################################


def init():

    # load all dh parameters
    for chainName, chain in dhChains.items():
        chain['chain'] = cJointChain(chain['dhParams'])


def updateDhChain():

    # calculate 3d locations of all chains
    # for chains having a predecessor use predecessors end position as start position
    for chainName, chain in dhChains.items():
        try:
            chain['chain'].dhCalc(chain['prevChain'])
        except Exception as e:
            config.log(f'problem calling dhCalc, {chain["name"]}, e: {e}')
            config.log(f"prevChain: {chain['prevChain']}")

    #config.log(f"dhChain updated", publish=False)

