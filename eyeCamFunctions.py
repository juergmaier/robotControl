

import sys
import time
import glob
import os

import numpy as np
import cv2
import face_recognition
from copy import deepcopy
from scipy.spatial import distance as dist
from collections import OrderedDict
import num2words as n2w
from dataclasses import dataclass

from PyQt5.QtCore import pyqtSlot, QThreadPool, QRunnable

import inmoovGlobal
import config
import arduinoSend
import i01
import camImages


MIN_ROTHEAD_DEGREES = -60
MAX_ROTHEAD_DEGREES = 60
ROTHEAD_SWIPE_STEP_DEGREES = 3

# for face recognition the encodings of the known persons
knownFacesEncodings=[]              # needed as list to pass into face_recognition

isFaceTrackingActive = False

imageNr = 0                   # numbered images
facesFolder = "faceImages"
facesFolderWithMarks = "faceImagesWithMarks"

newLocations = OrderedDict()
prevLocations = OrderedDict()
newFace = None
objectIdInRecognition = None
recognizedFaces = {}        # dict of KnownFace by objectId
unknownFaces = {}           # dict of unknown faces by objectId

class FaceTracking(QRunnable):
    @pyqtSlot()
    def run(self):
        locateFaces()


# von pyimagesearch
# tracking of persons in image sequences
# CAUTION: with more than 1 person an ID-Switch may occur
class CentroidTracker():
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



class FaceRecognition(QRunnable):
    @pyqtSlot()
    def run(self):
        recognizeFaces()


@dataclass()
class FaceFacts:
    name: str
    file: str
    encodingIndex: int
    announced: False


class KnownFaces:
    def __init__(self):
        self.knownFaces = []
        self.knownFacesEncoding = []

    def load(self):

        knownFacesFolder = "c:/Projekte/InMoov/robotControl/knownFaces"
        name = "Unknown"
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
                                    self.knownFaces.append(FaceFacts(folder, file, index, False))
                                    config.log(f"encoding found and loaded for: {folder}/{file}")

                            else:
                                # no encoding file exists, create it
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

                                encoding = face_recognition.face_encodings(image)
                                if len(encoding) == 1:
                                    np.save(encodingFile, encoding[0])
                                    config.log(f"encoding file created for: {folder}/{file}")
                                    self.knownFacesEncoding.append(encoding[0])
                                    self.knownFaces.append(FaceFacts(folder, file, index, False))
                    else:
                        config.log(f"unexpected folder structure in {knownFacesFolder}")


    def recognizeFace(self, faceImage):

        # a new face, compare it against the known faces
        unknownEncoding = face_recognition.face_encodings(faceImage)
        if len(unknownEncoding) == 0:
            config.log(f"could not create encoding for face")
            return None

        # compare the image against the known faces (returns indices of knownFacesEncodings)
        result = face_recognition.face_distance(self.knownFacesEncoding, unknownEncoding[0])

        if len(result) == 0:
            config.log(f"unknown person")
            return None
        else:
            # find best match (smallest eucledian distance of face properties)
            bestMatch = 1
            bestImage = None
            for i, match in enumerate(result):
                if match < bestMatch:
                    bestMatch = match
                    bestImage = i

            config.log(f"best match: {bestMatch:.2f}, name: {self.knownFaces[bestImage].name}, file: {self.knownFaces[bestImage].file}")
            return self.knownFaces[bestImage].name


class ScanForPeople:
    def __init__(self):
        self.rotheadCurrentDegrees = 0
        self.rotheadSwipeStepDegrees = 2
        self.rotheadMaxDegrees = 50
        self.rotheadMinDegrees = -50
        self.rotheadNewDegrees = 0

    def nextRotheadDegrees(self):
        self.rotheadCurrentDegrees
        self.rotheadNewDegrees  = config.servoCurrentDict['head.rothead'].degrees + self.rotheadSwipeStepDegrees
        #self.rotheadNewDegrees = self.rotheadNewDegrees + self.rotheadSwipeStepDegrees

        if self.rotheadNewDegrees > self.rotheadMaxDegrees:
            self.rotheadNewDegrees = self.rotheadMaxDegrees
            self.rotheadSwipeStepDegrees = -self.rotheadSwipeStepDegrees

        if self.rotheadNewDegrees < self.rotheadMinDegrees:
            self.rotheadNewDegrees = self.rotheadMinDegrees
            self.rotheadSwipeStepDegrees = -self.rotheadSwipeStepDegrees

        return self.rotheadNewDegrees


def xyOffsetFace(startX, startY, endX, endY, w, h):

    faceXCenter = (startX + endX) / 2
    xOffset = faceXCenter - (w/2)
    fovH = camImages.cams[inmoovGlobal.EYE_CAM].fovH
    faceXAngle = fovH / w * xOffset
    config.log(f"w: {w}, faceXCenter: {faceXCenter:.0f}, xOffset: {xOffset:.0f}, fovH: {fovH}, faceXAngle: {faceXAngle:.1f}")

    faceYCenter = (startY + endY) / 2
    yOffset = faceYCenter - (h/2)
    fovV = camImages.cams[inmoovGlobal.EYE_CAM].fovV
    faceYAngle = -fovV / h * yOffset
    config.log(f"h: {h}, faceYCenter: {faceYCenter:.0f}, yOffset: {yOffset:.0f}, fovV: {fovV}, faceYAngle: {faceYAngle:.1f}")

    return faceXAngle, faceYAngle


def locateFaces():
    '''
    this function is started as a thread from the gui (guiLogic.py)
    in this implementation a face tracker is added, trying to find the movements
    of all faces in relation to the last taken image.
    It also detects new faces in the image which can than be passed to the face recognizer
    '''
    global newLocations, prevLocations, objectIdInRecognition, newFace

    # find last image number used in faces folder to save images with a unique file name
    # this allows easier testing and can be ignored, if we have no interrest in the image history
    filesInFolder = glob.glob(facesFolder + "/*")
    if len(filesInFolder) == 0:
        imageNr = 0
    else:
        latestFile = max(filesInFolder, key=os.path.getctime)
        imageNr = int(os.path.basename(latestFile)[:-4]) + 1

    # verify cam
    config.eyecamFrame = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()
    w, h = config.eyecamFrame.shape[0:2]

    # create the person tracker
    tracker = CentroidTracker()
    scanForPeople = ScanForPeople()

    lastAnalysis = time.time()

    scanDelay = 5

    while isFaceTrackingActive:

        rects = []      # the bounding boxes of all faces in this image

        # limit analysis to 10/sec
        if time.time() - lastAnalysis < 0.1:
            time.sleep(lastAnalysis + 0.1 - time.time())

        lastAnalysis = time.time()

        #capture image
        config.eyecamFrame = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()

        if config.eyecamFrame is None:
            config.log(f"eyecam image not available")
            time.sleep(5)
            continue

        # downsize image to increase speed in face search
        faceFrame = cv2.resize(config.eyecamFrame, (240,320))
        #faceFrame = faceFrameBGR[:,:,::-1]

        h, w = faceFrame.shape[0:2]     #
        start = time.time()

        # Find all the faces in the current frame of video
        faceLocations = face_recognition.face_locations(faceFrame)

        #config.log(f"detection duration: {start - time.time()}")

        if len(faceLocations) == 0:
            config.log("face locator: keine Person erkannt")
            scanDelay -= 1
            if scanDelay == 0:
                newRotheadDegrees = scanForPeople.nextRotheadDegrees()
                arduinoSend.requestServoDegrees('head.rothead', newRotheadDegrees, 100, filterSequence=False)
                scanDelay = 2
                continue

        if len(faceLocations) == 1:
            config.log("face locator: eine Person erkannt")
            scanDelay = 5

        if len(faceLocations) > 1:
            config.log(f"face locator: {n2w.num2words(len(newLocations), lang='de')} personen erkannt")
            scanDelay = 5

        if len(faceLocations) > 0:

            # save the image for later replay (used for testing only)
            imageNr += 1
            cv2.imwrite(f"{facesFolder}/{imageNr:04.0f}.jpg", faceFrame)

            # add face areas in image to the rects list
            for top, right, bottom, left in faceLocations:
                rects.append((left, top, right, bottom))

                # for verification draw a box around each face
                cv2.rectangle(faceFrame, (left, top), (right, bottom), (0, 0, 255), 2)


            # update the tracker using face rectangles
            newLocations = tracker.update(rects)    # returns OrderedDict, face locations by objectId

            # loop over the tracked faces
            for (objectId, centroid) in newLocations.items():

                cX, cY, left, right, top, bottom = centroid

                # check for unknown person
                if objectId not in recognizedFaces:
                    config.log(f"face locator: unknown person detected")

                    # check for currently running face recognition
                    if objectIdInRecognition is None:

                        config.log(f"face locator: set image and flag for recognizer, objectId: {objectId}")
                        newFace = faceFrame[top:bottom, left:right]
                        objectIdInRecognition = objectId    # triggers face recognition
                    else:
                        config.log(f"face locator: face recognizer currently busy")

                else:
                    if not recognizedFaces[objectId].announced:
                        config.log(f"recognized person: {recognizedFaces[objectId].name}")
                        i01.mouth.speakBlocking(f"hallo {recognizedFaces[objectId].name}")
                        recognizedFaces[objectId].announced = True

                # for visualization add ID, face center and line of move to the frame
                text = "ID {}".format(objectId)
                cv2.putText(faceFrame, text, (cX - 10, cY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(faceFrame, (cX, cY), 4, (0, 255, 0), -1)

                if objectId in prevLocations:  # check for previous location known
                    cv2.line(faceFrame, (cX, cY),
                             (prevLocations[objectId][0], prevLocations[objectId][1]), (0, 255, 0), 2)
                    #print(f"line {centroid}, {prevLocations[objectId]}")



            # Display the results of first found face
            #for top, right, bottom, left in faceLocations:
            (top, right, bottom, left) = faceLocations[0]

            # save the image with markings
            cv2.imwrite(f"{facesFolderWithMarks}/{imageNr:04.0f}.jpg", faceFrame)

            # Display the resulting  image
            cv2.imshow('Face', faceFrame)
            cv2.waitKey(1)

            # move rothead and neck to center face in image
            # get current angles first
            config.log(f"image: {imageNr:04.0f}.jpg, {w}x{h}")
            faceXAngle, faceYAngle = xyOffsetFace(left, top, right, bottom, w, h)

            # It's assumed to be save to access the degrees value without locking
            # if a factor to dampen the moves is not good enough it might need a pid controller
            currRotheadDegrees = config.servoCurrentDict['head.rothead'].degrees

            # check for movement and try to compensate for it
            if len(prevLocations) == 0:
                prevLocations = deepcopy(newLocations)

            camMoveFactor = 0.8
            if abs(prevLocations[0][0] - newLocations[0][0]) > 10:        # x pixel change
                camMoveFactor = 1.2
            newRotheadDegrees = currRotheadDegrees + (camMoveFactor * faceXAngle)

            currNeckDegrees = config.servoCurrentDict['head.neck'].degrees
            # check for movement and try to compensate for it
            newNeckDegrees = currNeckDegrees + (0.8 * faceYAngle)

            config.log(
                f"currRotheadDegrees: {currRotheadDegrees:.0f}, faceXAngle: {faceXAngle:.0f}, newRotheadDegrees: {newRotheadDegrees:.0f}, currNeckDegrees: {currNeckDegrees:.0f}, faceYAngle: {faceYAngle:.0f},  newNeckDegrees: {newNeckDegrees:.0f}")

            # request new positions and do not filter requests as the situation can change quickly
            arduinoSend.requestServoDegrees('head.rothead', newRotheadDegrees, 100, filterSequence=False)
            arduinoSend.requestServoDegrees('head.neck', newNeckDegrees, 100, filterSequence=False)

            # use the new locations as the previous locations for the next image analysis
            prevLocations = deepcopy(newLocations)



def recognizeFaces():
    '''
    Thread started with locateFaces request
    Thread ends when isFaceTrackingActive is set to False
    When locateFaces detects a new person it requests a person search by setting "objectIdInRecognition"
    If the person is recognized, it adds the objectId and name to the recognizedFaces array
    '''

    global objectIdInRecognition, recognizedFaces

    knownFaces = KnownFaces()
    knownFaces.load()

    while isFaceTrackingActive:

        # check for new face to recognize
        if objectIdInRecognition is not None:

            config.log(f"new face passed to recognizer")

            person = knownFaces.recognizeFace(newFace)

            if person is None:
                unknownFaces.update({objectIdInRecognition: FaceFacts("", "", 0, False)})
            else:
                recognizedFaces.update({objectIdInRecognition: FaceFacts(person, "", 0, False)})

            # make recognition ready for another face to recognize
            objectIdInRecognition = None

        else:
            time.sleep(0.2)



def newFaceRecording():

    # give instructions and start recording
    instructions = """Hallo, ich bin Marvin und möchte einige Bilder von deinem Gesicht aufnehmen, damit ich dich später wiedererkennen kann.
    Bitte stelle dich ca. eins komma fuenf Meter vor mich hin und schau mir in die Augen.
    Falls eine Aufnahme nicht passt, werde ich dir Anweisungen geben, wie du dich bewegen solltest.
    Die Kamera darf nur deinen eigenen Kopf erfassen, nicht auch andere Personen.
    Es werden 5 Bilder im Abstand von einer Sekunde gemacht, es werden aber nur passende Bilder abgelegt.
    Während der Aufnahme solltest du stehen bleiben und mir in das rechte Auge sehen, lächeln nicht vergessen.
    """
    skipIntro = False
    if not skipIntro:
        i01.mouth.speakBlocking(instructions)

    for i in range(5):
        config.eyecamFrame = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()
        cv2.imshow("eyeCam", config.eyecamFrame)
        cv2.waitKey(1000)

    newFaceFolder = "newFace"

    # check for folder exists
    if not os.path.exists(newFaceFolder):
        os.mkdir(newFaceFolder)

    # remove all files in newFaceFolder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(BASE_DIR, newFaceFolder)

    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            os.remove(path)


    # take a picture every second and store it in folder "newFace"
    imageNr = 0
    failures = 0
    i01.mouth.speakBlocking("es geht los")

    numPic = 5

    while imageNr < numPic:

        frameText = "unpassendes Bild"

        image = camImages.cams[inmoovGlobal.EYE_CAM].takeImage()
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

                faceXAngle, faceYAngle = xyOffsetFace(left, top, right, bottom, w, h)

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
                    i01.mouth.speakBlocking(f"Bild {n2w.num2words(imageNr, lang='de')} von {n2w.num2words(numPic, lang='de')} erfolgreich aufgenommen")
                    imageNr += 1

                else:
                    # Draw a box around the face
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow(frameText, image)
        cv2.waitKey(500)
        cv2.destroyAllWindows()


    i01.mouth.speakBlocking("das war's, vielen dank")
    return True
