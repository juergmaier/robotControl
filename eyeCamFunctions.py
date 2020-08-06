

import time
import datetime
from dateutil.relativedelta import relativedelta
import glob
import os
import simplejson as json

import numpy as np
import cv2
import face_recognition
from copy import deepcopy
from scipy.spatial import distance as dist
from collections import OrderedDict
import num2words as n2w
from dataclasses import dataclass

from PyQt5.QtCore import pyqtSlot, QRunnable

import inmoovGlobal
import config
import arduinoSend
import i01
import camImages


MIN_ROTHEAD_DEGREES = -60
MAX_ROTHEAD_DEGREES = 60
ROTHEAD_SWIPE_STEP_DEGREES = 3

# for face recognition the encodings of the known persons
knownFacesEncodings = []              # needed as list to pass into face_recognition

isFaceTrackingActive = False

facesFolder: str = "faceImages"
facesFolderWithMarks: str = "faceImagesWithMarks"


# von pyimagesearch
# tracking of persons in image sequences
# CAUTION: with more than 1 person an ID-Switch may occur
class PersonTracker:
    def __init__(self, maxDisappeared=50):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        # store the number of maximum consecutive frames a given
        # object is allowed to be marked as "disappeared" until we
        # need to deregister the object from tracking
        self.maxDisappeared = maxDisappeared


    def register(self, centroid):
        # when registering an object we use the next available object
        # ID to store the centroid
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectId):
        # to deregister an object ID we delete the object ID from
        # both of our respective dictionaries
        del self.objects[objectId]
        del self.disappeared[objectId]


    def update(self, rects) -> OrderedDict:
        # check to see if the list of input bounding box rectangles
        # is empty
        if len(rects) == 0:
            # loop over any existing tracked objects and mark them
            # as disappeared
            for objectId in list(self.disappeared.keys()):
                self.disappeared[objectId] += 1
                # if we have reached a maximum number of consecutive
                # frames where a given object has been marked as
                # missing, deregister it
                if self.disappeared[objectId] > self.maxDisappeared:
                    self.deregister(objectId)
            # return early as there are no centroids or tracking info
            # to update
            return self.objects

        # initialize an array of input centroids for the current frame
        inputCentroids = np.zeros((len(rects), 6), dtype="int")
        # loop over the bounding box rectangles
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY, startX, endX, startY, endY)

        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])

        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            objectIds = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            # compute the distance between each pair of object
            # centroids and input centroids, respectively -- our
            # goal will be to match an input centroid to an existing
            # object centroid
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            # in order to perform this matching we must (1) find the
            # smallest value in each row and then (2) sort the row
            # indexes based on their minimum values so that the row
            # with the smallest value is at the *front* of the index
            # list
            rows = D.min(axis=1).argsort()
            # next, we perform a similar process on the columns by
            # finding the smallest value in each column and then
            # sorting using the previously computed row index list
            cols = D.argmin(axis=1)[rows]


            # in order to determine if we need to update, register,
            # or deregister an object we need to keep track of which
            # of the rows and column indexes we have already examined
            usedRows = set()
            usedCols = set()
            # loop over the combination of the (row, column) index
            # tuples
            for (row, col) in zip(rows, cols):
                # if we have already examined either the row or
                # column value before, ignore it
                # val
                if row in usedRows or col in usedCols:
                    continue
                # otherwise, grab the object ID for the current row,
                # set its new centroid, and reset the disappeared
                # counter
                objectId = objectIds[row]
                self.objects[objectId] = inputCentroids[col]
                self.disappeared[objectId] = 0
                # indicate that we have examined each of the row and
                # column indexes, respectively
                usedRows.add(row)
                usedCols.add(col)


            # compute both the row and column index we have NOT yet
            # examined
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)


            # in the event that the number of object centroids is
            # equal or greater than the number of input centroids
            # we need to check and see if some of these objects have
            # potentially disappeared
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # grab the object ID for the corresponding row
                    # index and increment the disappeared counter
                    objectId = objectIds[row]
                    self.disappeared[objectId] += 1
                    # check to see if the number of consecutive
                    # frames the object has been marked "disappeared"
                    # for warrants deregistering the object
                    if self.disappeared[objectId] > self.maxDisappeared:
                        self.deregister(objectId)

            # otherwise, if the number of input centroids is greater
            # than the number of existing object centroids we need to
            # register each new input centroid as a trackable object
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])


        # return the set of trackable objects
        return self.objects


"""
class FaceRecognition(QRunnable):
    @pyqtSlot()
    def run(self):
        recognizeFaces()
"""

@dataclass()
class FaceFacts:
    name: str
    file: str
    encodingIndex: int
    announced: bool             # person greeted
    lastVerification : float    # for repeating person recognition to verify faceId->name relation


class KnownFaces:
    def __init__(self):
        self.knownFaces = []
        self.knownFacesEncoding = []

    def load(self):

        knownFacesFolder = "c:/Projekte/InMoov/robotControl/knownFaces"

        for folder in os.listdir(knownFacesFolder):
            folderPath = os.path.join(knownFacesFolder, folder)
            if os.path.isfile(folderPath):
                config.log(f"unexpected folder structure in {knownFacesFolder}")
            else:
                for index, file in enumerate(os.listdir(folderPath)):
                    fullPath = os.path.join(folderPath, file)
                    if os.path.isfile(fullPath):
                        if fullPath.endswith(".jpg"):

                            # check for existing encoding file
                            encodingFile = fullPath[:-4] + ".npy"
                            if os.path.isfile(fullPath[:-4] + ".npy"):
                                with open(encodingFile, 'rb') as f:
                                    self.knownFacesEncoding.append(np.load(f))
                                    self.knownFaces.append(FaceFacts(folder, file, index, False, 0))
                                    config.log(f"knownFaces, encoding found and loaded for: {folder}/{file}")

                            else:
                                # no encoding file exists, create it
                                config.log(f"try to create encoding for file: {fullPath}")
                                image = face_recognition.load_image_file(f"{fullPath}")
                                w,h = image.shape[:2]
                                top, right, bottom, left = face_recognition.face_locations(image)[0]

                                # show box in image
                                #cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                                #cv2.imshow("boxed face", image)

                                frameWidth = 40
                                left1 = left-frameWidth if left > frameWidth else 0
                                top1 = top-frameWidth if top > frameWidth else 0
                                right1 = right+frameWidth if right+frameWidth < w else w
                                bottom1 = bottom+frameWidth if bottom+frameWidth < h else h
                                faceImage = image[top1:bottom1, left1:right1]
                                #cv2.imshow("face only", faceImage)
                                #cv2.waitKey(500)

                                encoding = face_recognition.face_encodings(faceImage)
                                if len(encoding) == 1:
                                    np.save(encodingFile, encoding[0])
                                    config.log(f"encoding file created for: {folder}/{file}")
                                    self.knownFacesEncoding.append(encoding[0])
                                    self.knownFaces.append(FaceFacts(folder, file, index, False, time.time()))
                    else:
                        config.log(f"unexpected folder structure in {knownFacesFolder}")


    def recognizeThisFace(self, faceImage):

        # a new face, compare it against the known faces
        unknownEncoding = face_recognition.face_encodings(faceImage)
        if len(unknownEncoding) == 0:
            config.log(f"face recognizer: could not create encoding for face")
            return None

        config.log(f"face recognizer: encoding for face created")
        # compare the image against the known faces (returns indices of knownFacesEncodings)
        result = face_recognition.face_distance(self.knownFacesEncoding, unknownEncoding[0])

        if len(result) == 0:
            config.log(f"face recognizer: unknown person")
            return None
        else:
            # find best match (smallest eucledian distance of face properties)
            bestMatch = 1
            bestImage = None
            for i, match in enumerate(result):
                if match < bestMatch:
                    bestMatch = match
                    bestImage = i

            if bestMatch > 0.7:
                config.log(f"face recognizer: unknown person, best match: {bestMatch:.2f}")
                return None

            config.log(f"face recognizer: best match: {bestMatch:.2f}, name: {self.knownFaces[bestImage].name}, file: {self.knownFaces[bestImage].file}")
            return self.knownFaces[bestImage].name


class ScanForPerson:
    def __init__(self, faceTracking):
        self.faceTracking = faceTracking    # handle to outer class
        self.scanActive = False
        self.startRotheadMove = time.time()
        self.camSteadyDuration = 0.5
        self.rotheadSwipeStepDegrees = 5
        self.rotheadMaxDegrees = 50
        self.rotheadMinDegrees = -50
        self.rotheadNextDegrees = 0


    def scan(self):
        if not self.scanActive:
            self.scanActive = True
            config.log(f"scan for person started")
            i01.mouth.speakBlocking("ich suche nach personen")

            # set default positions of eyes and neck for scan
            self.faceTracking.moveCam('head.eyeX', 0, 50)
            self.faceTracking.moveCam('head.eyeY', 0, 50)
            self.faceTracking.moveCam('head.neck', -10, 500)

        self.setRotheadNextDegrees()


    def setRotheadNextDegrees(self):
        self.rotheadNextDegrees = config.servoCurrentDict['head.rothead'].degrees + self.rotheadSwipeStepDegrees
        #self.rotheadNewDegrees = self.rotheadNewDegrees + self.rotheadSwipeStepDegrees

        if self.rotheadNextDegrees > self.rotheadMaxDegrees:
            self.rotheadNextDegrees = self.rotheadMaxDegrees
            self.rotheadSwipeStepDegrees = -self.rotheadSwipeStepDegrees

        if self.rotheadNextDegrees < self.rotheadMinDegrees:
            self.rotheadNextDegrees = self.rotheadMinDegrees
            self.rotheadSwipeStepDegrees = -self.rotheadSwipeStepDegrees


    def stopScan(self):
        self.scanActive = False
        config.log(f"scan for person stopped")
        i01.mouth.speakBlocking("eine person gesehen")


class CenterOnPerson:
    """
    move eye and head servos to center person in image
    """

    def __init__(self, faceTracking):
        self.faceTracking = faceTracking    # handle to outer class
        self.moveEyeX = False
        self.moveEyeY = False
        self.moveRothead = False
        self.moveNeck = False
        self.moveStartTime = time.time()
        self.eyeXDampFactor = 0.5
        self.eyeYDampFactor = 0.3


    @staticmethod
    def calcRotheadCorrection(faceXAngle, faceWidth):

        # use face width to get an approximate distance to the person
        faceWidthDegrees = camImages.cams[inmoovGlobal.EYE_CAM].fovH / 240 * faceWidth
        faceWidthInCm = 16
        approxDist = faceWidthInCm / np.tan(np.radians(faceWidthDegrees))
        config.log(f"faceWidth: {faceWidth}, faceWidthDegrees: {faceWidthDegrees:.1f}, approxDist: {approxDist:.0f}")

        # from current angles of rothead and eyeX and the approxDist calc new rothead angle with eyeX-Angle 0
        d1 = np.tan(np.radians(faceXAngle)) * approxDist
        d2 = np.sqrt(approxDist * approxDist - d1 * d1)
        d3 = d2 + 13  # 13 is distance from eye to rothead
        correction = np.degrees(np.arctan(d1 / d3))
        config.log(f"rothead correction: {correction:.1f} degrees")

        return correction


    def adjustCam(self, faceXAngle, faceYAngle, faceWidth):

        # It's assumed to be save to access the degrees value without locking
        # if a factor to dampen the moves is not good enough it might need a pid controller
        currRotheadDegrees = config.servoCurrentDict['head.rothead'].degrees
        currNeckDegrees = config.servoCurrentDict['head.neck'].degrees
        currEyeXDegrees = config.servoCurrentDict['head.eyeX'].degrees
        currEyeYDegrees = config.servoCurrentDict['head.eyeY'].degrees

        # if person is already close to the image center check for center exeX and compensate with rothead
        if abs(faceXAngle) < 3:

            # check for high eyeX offset
            if abs(currEyeXDegrees) > 5:
                config.log(f"zero eyeX and move rothead, faceXAngle: {faceXAngle:.1f}, currEyeXDegrees: {currEyeXDegrees:.1f}")

                corrAngleRothead = self.calcRotheadCorrection(faceXAngle, faceWidth)
                newRotheadDegrees = currRotheadDegrees + corrAngleRothead
                self.moveStartTime = time.time()
                self.faceTracking.moveCam('head.eyeX', 0, 80)
                self.faceTracking.moveCam('head.rothead', newRotheadDegrees, 80)

        # if person is off center and eye movement is still possible try to follow with eye
        elif abs(faceXAngle) < 8 and abs(currEyeXDegrees) < 10:
            newEyeXDegrees = currEyeXDegrees + (faceXAngle * self.eyeXDampFactor)
            config.log(f"center person in image with eyeX move, newEyeX: {newEyeXDegrees:.1f}, faceXAngle: {faceXAngle:.1f}")
            self.moveStartTime = time.time()
            self.faceTracking.moveCam('head.eyeX', newEyeXDegrees, 30)
            self.moveEyeX = True

        else:  # move rothead to center on person, move eyeX to 0 within same time span
            config.log(f"center person in image with rothead: {faceXAngle:.1f}, currEyeXDegrees: {currEyeXDegrees:.1f}")
            corrAngleRothead = self.calcRotheadCorrection(faceXAngle, faceWidth)
            newRotheadDegrees = currRotheadDegrees + corrAngleRothead

            self.faceTracking.moveCam('head.eyeX', 0, 80)
            self.faceTracking.moveCam('head.rothead', newRotheadDegrees, 80)

        # check for needed neck move
        if abs(faceYAngle) < 2:
            # person is close to image center, check for eyeY offset
            if abs(currEyeYDegrees) > 3:
                config.log(f"zero eyeY and move neck: {faceYAngle:.1f}, currEyeYDegrees: {currEyeYDegrees:.1f}")
                newNeckDegrees = currNeckDegrees + faceYAngle + (currEyeYDegrees * self.eyeYDampFactor)

                self.faceTracking.moveCam('head.eyeY', 0, 80)
                self.faceTracking.moveCam('head.neck', newNeckDegrees, 80)


        # if person is off center and eye movement is still possible follow with eye first
        elif abs(faceYAngle) < 8 and abs(currEyeYDegrees) < 10:
            newEyeYDegrees = currEyeYDegrees - faceYAngle * self.eyeYDampFactor
            config.log(f"center person in image with eyeY move: {newEyeYDegrees:.1f}, faceYAngle: {faceYAngle:.1f}")

            self.faceTracking.moveCam('head.eyeY', newEyeYDegrees, 30)


        else:  # move neck to center on person, move eyeY to 0 within same time span
            config.log(f"center person in image with neck: {faceYAngle:.1f}, currEyeYDegrees: {currEyeYDegrees:.1f}")
            newNeckDegrees = currNeckDegrees + faceYAngle + currEyeYDegrees * self.eyeYDampFactor

            self.faceTracking.moveCam('head.eyeY', 0, 80)
            self.faceTracking.moveCam('head.neck', newNeckDegrees, 80)



def copyFaceFromImage(image, faceStartLeft, faceEndRight, faceStartTop, faceEndBottom):
    # add a frame area around the face rectangle to get a more complete picture of the person
    w, h = image.shape[0:2]
    frameWidth = int(0.3 * (faceEndRight - faceStartLeft))
    left1 = faceStartLeft - frameWidth if faceStartLeft > frameWidth else 0
    top1 = faceStartTop - frameWidth if faceStartTop > frameWidth else 0
    right1 = faceEndRight + frameWidth if faceEndRight + frameWidth < w else w
    bottom1 = faceEndBottom + frameWidth if faceEndBottom + frameWidth < h else h

    return image[top1:bottom1, left1:right1].copy()


class FaceTracking(QRunnable):
    """
    this function is started as a thread from the gui (guiLogic.py)
    in this implementation a face tracker is added, trying to find the movements
    of all faces in relation to the last taken image.
    It also detects new faces in the image which can than be passed to the face recognizer
    """
    #@pyqtSlot()

    def __init__(self):
        super().__init__()
        self.newLocations = OrderedDict()
        self.prevLocations = OrderedDict()
        self.faceToRecognize = None
        self.faceIdInRecognition = None
        self.recognizedFaces = {}  # dict of recognized faces by faceId
        self.unknownFaces = {}  # dict of unknown faces by faceIdId
        self.imageNr = self.evalNextImageNumber()

        # create the person tracker
        self.tracker = PersonTracker()
        self.scanForPerson = ScanForPerson(self)
        self.centerOnPerson = CenterOnPerson(self)
        self.timeLastPersonDetected = time.time()
        self.camMoveStartTime = 0
        self.camMoveHead = False
        self.camMoveEye = False
        self.rotheadDegreesImage = 0

        # verify cam
        _ = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()  # verify available cam


    @staticmethod
    def xyOffsetFace(startX, startY, endX, endY, w, h):

        faceXCenter = (startX + endX) / 2
        xOffset = faceXCenter - (w / 2)
        fovH = camImages.cams[inmoovGlobal.EYE_CAM].fovH
        faceXAngle = fovH / w * xOffset
        config.log(
            f"centerFace, startX: {startX}, endX: {endX}, w: {w}, faceXCenter: {faceXCenter:.0f}, xOffset: {xOffset:.0f}, fovH: {fovH}, faceXAngle: {faceXAngle:.1f}")

        faceYCenter = (startY + endY) / 2
        yOffset = faceYCenter - (h / 2)
        fovV = camImages.cams[inmoovGlobal.EYE_CAM].fovV
        faceYAngle = -fovV / h * yOffset
        config.log(
            f"centerFace, startY: {startY}, endY: {endY}, h: {h}, faceYCenter: {faceYCenter:.0f}, yOffset: {yOffset:.0f}, fovV: {fovV}, faceYAngle: {faceYAngle:.1f}")

        return faceXAngle, faceYAngle


    def evalNextImageNumber(self):
        # find last image number used in faces folder to save images with a unique file name
        # this allows easier testing and can be ignored, if we have no interrest in the image history
        filesInFolder = glob.glob(facesFolder + "/*")
        if len(filesInFolder) == 0:
            return 0
        else:
            latestFile = max(filesInFolder, key=os.path.getctime)
            return int(os.path.basename(latestFile)[:-4]) + 1


    def waitForSteadyCam(self):
        # depending on servos moved wait for a steady cam image
        if self.camMoveHead:
            requestedRotheadDegrees = self.scanForPerson.rotheadNextDegrees

            # wait with timeout for rothead to move to requested degrees
            while time.time() - self.camMoveStartTime < 2:
                # check actual position matches expected position
                # this is inaccureate because we do not have a measured servo position available
                currentRotheadDegrees = config.servoCurrentDict['head.rothead'].degrees
                if abs(currentRotheadDegrees - requestedRotheadDegrees) < 2:
                    break
                time.sleep(0.05)
            config.log(f"rothead moved in {time.time()-self.camMoveStartTime:.2f} s to {currentRotheadDegrees}")
            time.sleep(0.2)

        if self.camMoveEye:
            # for eye moves wait a fixed time
            while time.time() - self.camMoveStartTime < 0.4:
                time.sleep(0.05)

        self.camMoveHead = False
        self.camMoveEye = False


    def moveCam(self, servoName, degrees, duration):
        #config.log(f"moveCam, {servoName}, degrees: {degrees} ")
        arduinoSend.requestServoDegrees(servoName, degrees, duration, filterSequence=False)
        if servoName in ['head.rothead', 'head.neck']:
            self.camMoveHead = True
        else:
            self.camMoveEye = True
        self.camMoveStartTime = time.time()


    def writeLastSeenFile(self, lastSeenFile):
        # update last seen timestamp in person folder
        with open(lastSeenFile, 'w') as outfile:
            json.dump(datetime.datetime.fromtimestamp(time.time()), outfile, default=str)


    def addOrRemovePerson(self, person):
        '''
        called by face recognizer thread that tries to identify the faceIdInRecognition
        :param person: name of the recognized person or None
        '''
        # check for new or already recognized person
        if person is None:
            # the face is unknown, check if it was recognized before
            if self.faceIdInRecognition in self.recognizedFaces:
                # if the faceId is unknown now remove it from the recognizedFaces dict
                del self.recognizedFaces[self.faceIdInRecognition]
            # add or update the face facts in the unknownFaces dict
            self.unknownFaces.update({self.faceIdInRecognition: FaceFacts("", "", 0, False, time.time())})
        else:
            # the faceId is attached to a person, check for switch of the person behind this faceId
            if self.faceIdInRecognition in self.recognizedFaces:
                if person != self.recognizedFaces[self.faceIdInRecognition].name:
                    # the faceId is now bound to another person, update the person in the recognized faces dict
                    config.log(f"faceId changed for {person}")
                    self.recognizedFaces.update(
                        {self.faceIdInRecognition: FaceFacts(person, "", 0, False, time.time())})
                else:
                    self.recognizedFaces[self.faceIdInRecognition].lastVerification = time.time()
            else:
                self.recognizedFaces.update(
                    {self.faceIdInRecognition: FaceFacts(person, "", 0, False, time.time())})


    def run(self):
        while isFaceTrackingActive:

            rects = []      # the bounding boxes of all faces in this image

            # capture image
            self.waitForSteadyCam()

            config.eyecamImage = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()   # capture image for tracking
            self.rotheadDegreesImage = config.servoCurrentDict['head.rothead'].degrees
            self.eyeXDegreesImage = config.servoCurrentDict['head.eyeX'].degrees

            self.imageNr += 1
            config.log(f"eyecam image taken {self.imageNr}, rothead: {self.rotheadDegreesImage} degrees, eyeX: {self.eyeXDegreesImage}")

            # in scan mode start move to next scan position while we analyze the last taken image
            if self.scanForPerson.scanActive:
                self.scanForPerson.scan()
                self.moveCam('head.rothead', self.scanForPerson.rotheadNextDegrees, 80)

            # for testing only: load image
            #config.eyecamFrame = cv2.imread(f'{facesFolder}/1108.jpg')

            cv2.imshow("eyeCam", config.eyecamImage)
            cv2.waitKey(1)
            snapFileName = f"{facesFolder}/{self.imageNr:4.0f}.jpg"
            cv2.imwrite(snapFileName, config.eyecamImage)

            if config.eyecamImage is None:
                config.log(f"eyecam image not available")
                time.sleep(5)
                continue

            # downsize image to increase speed in face search
            faceFrame = cv2.resize(config.eyecamImage, (240, 320))
            #faceFrame = faceFrameBGR[:,:,::-1]

            h, w = faceFrame.shape[0:2]     #
            #start = time.time()

            # Find all the faces in the current frame of video
            faceLocations = face_recognition.face_locations(faceFrame)

            #config.log(f"detection duration: {start - time.time()}")

            if len(faceLocations) == 0:
                config.log("face locator: no person located")

                # if we are not scanning (rothead) retry to locate faces with current rothead
                if not self.scanForPerson.scanActive:
                    if time.time() - self.timeLastPersonDetected < 2:
                        config.log(f"face locator: no person detected but not in scan and no timeout, retry")
                        continue

                    config.log(f"face locator: time since last person seen: {time.time()-self.timeLastPersonDetected:.2f}, resume scan")
                    self.scanForPerson.scan()
                    continue


            if len(faceLocations) == 1:
                config.log("face locator: located 1 person")

            if len(faceLocations) > 1:
                config.log(f"face locator: located {len(self.newLocations)} persons")

            if len(faceLocations) > 0:

                if self.scanForPerson.scanActive:
                    self.scanForPerson.stopScan()

                    # go back to rothead degrees of image
                    config.log(f"return rothead to detected person")
                    self.moveCam('head.rothead', self.rotheadDegreesImage, 50)
                    self.waitForSteadyCam()
                    #i01.mouth.speakBlocking("jemanden gefunden")

                self.timeLastPersonDetected = time.time()

                # save the image for later replay (used for testing only)
                #imageNr += 1
                #cv2.imwrite(f"{facesFolder}/{imageNr:04.0f}.jpg", faceFrame)

                # add face areas in image to the rects list
                for top, right, bottom, left in faceLocations:
                    rects.append((left, top, right, bottom))

                    # for verification draw a box around each face
                    #cv2.rectangle(faceFrame, (left, top), (right, bottom), (0, 0, 255), 2)


                # update the tracker using face rectangles
                newLocations = self.tracker.update(rects)    # returns OrderedDict, face locations by objectId

                # loop over the tracked faces
                for (faceId, centroid) in newLocations.items():

                    cX, cY, left, right, top, bottom = centroid

                    # check for already identified person
                    if faceId in self.recognizedFaces:

                        person = self.recognizedFaces[faceId].name
                        config.log(f"already identified person: {person}")

                        # check for greeting done
                        if not self.recognizedFaces[faceId].announced:
                            config.log(f"recognized person: {person}")
                            i01.mouth.speakBlocking(f"hallo {person}")
                            self.recognizedFaces[faceId].announced = True

                            # check for last seen file
                            # special handling of jsonized datatime necessary, json.load() will fail
                            lastSeenFile = f"c:/projekte/inmoov/robotControl/knownFaces/{person}/lastSeen.json"
                            if os.path.exists(lastSeenFile):
                                #config.log(f"json file exists")
                                f = open(lastSeenFile, 'r')
                                content = f.read()      # json.dump adds "\ to the datetime
                                try:
                                    lastSeen = datetime.datetime.strptime(content[3:-3], '%y-%m-%d %H:%M:%S.%f')
                                    diff = relativedelta(datetime.datetime.fromtimestamp(time.time()), lastSeen)
                                    diffTxt, diffSpan, diffSince = config.shortTimeDiff(diff, 'ymdHMS', numSpans=2)
                                    config.log(f"last seen: {lastSeen}, {diffTxt}, {diffSpan}, {diffSince}")
                                    if cX % 2 == 0:
                                        i01.mouth.speakBlocking(f"ich habe dich seit {diffSince} nicht mehr gesehen")
                                    else:
                                        i01.mouth.speakBlocking(f"ich habe dich vor {diffSpan} das letzte mal gesehen")

                                except Exception as e:
                                    config.log(f"conversion of last seen date failed {e}, date: {content}")

                            else:
                                i01.mouth.speakBlocking(f"ich habe keine Aufzeichnung, wann ich dich das letzte mal gesehen habe.")

                            self.writeLastSeenFile(lastSeenFile)


                        # check for repeated name verification
                        if time.time() - self.recognizedFaces[faceId].lastVerification > 5:
                            # verify that we still have the same person attached to objectId
                            if self.faceIdInRecognition is None:
                                self.faceToRecognize = copyFaceFromImage(faceFrame, left, right, top, bottom)
                                self.faceIdInRecognition = faceId    # triggers face recognition

                    else:
                        config.log(f"face locator: unknown person detected")

                        # check for currently running face recognition
                        if self.faceIdInRecognition is None:
                            config.log(f"face locator: pass image to recognizer, objectId: {faceId}")

                            self.faceToRecognize = copyFaceFromImage(faceFrame, left, right, top, bottom)

                            self.faceIdInRecognition = faceId    # triggers face recognition

                        else:
                            config.log(f"face locator: face recognizer currently busy")


                    # for visualization add ID, face center and line of move to the frame
                    text = "ID {}".format(faceId)
                    cv2.putText(faceFrame, text, (cX - 10, cY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.circle(faceFrame, (cX, cY), 4, (0, 255, 0), -1)

                    if faceId in self.prevLocations:  # check for previous location known
                        cv2.line(faceFrame, (cX, cY),
                                 (self.prevLocations[faceId][0], self.prevLocations[faceId][1]), (0, 255, 0), 2)
                        #print(f"line {centroid}, {prevLocations[objectId]}")

                # Display the results of first found face
                #for top, right, bottom, left in faceLocations:
                (top, right, bottom, left) = faceLocations[0]

                # move eyes and head to center face in image
                # get current angles first
                config.log(f"image: {self.imageNr:04.0f}.jpg, {w}x{h}")
                faceXAngle, faceYAngle = FaceTracking.xyOffsetFace(left, top, right, bottom, w, h)

                # check for movement, use new locations as prevLocations in case we are in the first pass
                if len(self.prevLocations) == 0:
                    self.prevLocations = deepcopy(self.newLocations)

                # if person is close to image center and eye has an offset reduce eye offset with rothead move
                faceWidth = right - left
                self.centerOnPerson.adjustCam(faceXAngle, faceYAngle, faceWidth)

                # use the new locations as the previous locations for the next image analysis
                self.prevLocations = deepcopy(self.newLocations)



class RecognizeFaces(QRunnable):
    """
    Thread started with locateFaces request
    Thread ends when isFaceTrackingActive is set to False
    When locateFaces detects a new person it requests a person search by setting "objectIdInRecognition"
    If the person is recognized, it adds the objectId and name to the recognizedFaces array
    """
    def __init__(self, faceTracking):
        super().__init__()
        self.faceTracking = faceTracking
        #self.recognizedFaces = []
        self.faceToRecognize = None
        self.knownFaces = KnownFaces()
        self.knownFaces.load()
        self.unknownFaces = {}

    def run(self):

        while isFaceTrackingActive:

            # check for new face to recognize
            if self.faceTracking.faceIdInRecognition is not None:

                config.log(f"new request for face recognition")

                person = self.knownFaces.recognizeThisFace(self.faceTracking.faceToRecognize)

                self.faceTracking.addOrRemovePerson(person)

                # make recognition ready for another face to recognize
                self.faceTracking.faceIdInRecognition = None

            else:
                time.sleep(0.2)


def stopFaceTracking():

    global isFaceTrackingActive

    isFaceTrackingActive = False

    # reset autoDetach time for eye servo to normal
    arduinoSend.setAutoDetach('head.eyeX', 1000)
    arduinoSend.requestServoDegrees('head.eyeX', 0, 500)
    arduinoSend.requestServoDegrees('head.eyeY', 0, 500)
    arduinoSend.requestServoDegrees('head.rothead', 0, 500)
    arduinoSend.requestServoDegrees('head.neck', 0, 500)

    i01.mouth.speakBlocking("gesichtsverfolgung beendet")



def newFaceRecording():

    # give instructions and start recording
    instructions = """Hallo, ich bin Marvin und möchte einige Bilder von deinem Gesicht aufnehmen, damit ich dich später wiedererkennen kann.
    Bitte stelle dich ca. eins komma fuenf Meter vor mich hin und schau mir in die Augen.
    Falls eine Aufnahme nicht passt, werde ich dir Anweisungen geben, wie du dich bewegen solltest.
    Die Kamera darf nur deinen eigenen Kopf erfassen, nicht auch andere Personen.
    Es werden 5 Bilder im Abstand von einer Sekunde gemacht, es werden aber nur passende Bilder abgelegt.
    Während der Aufnahme solltest du stehen bleiben und mir in das Gesicht sehen, lächeln nicht vergessen.
    """
    skipIntro = True
    if not skipIntro:
        i01.mouth.speakBlocking(instructions)

    arduinoSend.requestServoDegrees('head.rothead', 0, 500)
    arduinoSend.requestServoDegrees('head.neck', -10, 500)
    for i in range(5):
        image = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()   # init new person recording
        cv2.imshow("eyeCam", image)
        cv2.waitKey(1000)

    newFaceFolder = "newFace"

    # check for folder exists
    if not os.path.exists(newFaceFolder):
        os.mkdir(newFaceFolder)

    # remove all files in newFaceFolder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(BASE_DIR, newFaceFolder)

    for root, dirs, files in os.walk(base):
        for file in files:
            path = os.path.join(base, file)
            os.remove(path)


    # take a picture every second and store it in folder "newFace"
    imageNr = 0
    failures = 0
    i01.mouth.speakBlocking("es geht los")

    numPic = 5

    while imageNr < numPic:

        frameText = "unpassendes Bild"

        image = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()    # new person recording
        w, h = image.shape[0:2]

        faceLocations = face_recognition.face_locations(image)

        #config.log(f"detection duration: {start - time.time()}")

        if len(faceLocations) == 0:
            i01.mouth.speakBlocking("kein Gesicht erkannt")
            failures += 1
            if failures > 5:
                i01.mouth.speakBlocking("Aufzeichung abgebrochen")
                return False

        if len(faceLocations) > 1:
            i01.mouth.speakBlocking("es darf sich nur eine Person im Bereich der Kamera befinden")

        if len(faceLocations) == 1:
            failures = 0

            # box the face
            for top, right, bottom, left in faceLocations:

                faceXAngle, faceYAngle = FaceTracking.xyOffsetFace(left, top, right, bottom, w, h)

                # check for valid face position in frame
                validPosition = True

                currRotheadDegrees = config.servoCurrentDict['head.rothead'].degrees
                currNeckDegrees = config.servoCurrentDict['head.neck'].degrees

                arduinoSend.requestServoDegrees('head.rothead', currRotheadDegrees+faceXAngle, 200)

                arduinoSend.requestServoDegrees('head.neck', currNeckDegrees+faceYAngle, 200)

                if right - left > 130:
                    validPosition = False
                    i01.mouth.speakBlocking("bitte etwas zurücktreten")

                if validPosition == True:

                    frameWidth = 40
                    left1 = left - frameWidth if left > frameWidth else 0
                    top1 = top - frameWidth if top > frameWidth else 0
                    right1 = right + frameWidth if right + frameWidth < w else w
                    bottom1 = bottom + frameWidth if bottom + frameWidth < h else h
                    faceWithFrame = image[top1:bottom1, left1:right1]

                    cv2.imwrite(f"{newFaceFolder}/{imageNr:02.0f}.jpg", faceWithFrame)
                    frameText = "Bild {imageNr} von {numPic}"
                    i01.mouth.speakBlocking(f"Bild {n2w.num2words(imageNr+1, lang='de')} von {n2w.num2words(numPic, lang='de')} erfolgreich aufgenommen")
                    imageNr += 1

                else:
                    # Draw a box around the face
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow(frameText, image)
        cv2.waitKey(500)
        cv2.destroyAllWindows()


    i01.mouth.speakBlocking("das war's, vielen dank")
    return True
