
import datetime
import numpy as np
import cv2
import imutils
import pyrealsense2 as rs

cams = {}

streamD415 = None
D415streaming = False
pc = None

def log(msg):
    logtime = str(datetime.datetime.now())[11:23]
    print(f"{logtime} - camImages - {msg}")


class Camera(object):

    def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, numReads):
        self.name = name
        self.deviceId = deviceId
        self.cols = cols
        self.rows = rows
        self.fovH = fovH
        self.fovV = fovV
        self.rotate = rotate
        self.numReads = numReads

        self.handle = None
#        self.img = None



class UsbCamera(Camera):
    def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, initialReads):
        super().__init__(name, deviceId, cols, rows, fovH, fovV, rotate, initialReads)

        try:
            self.handle = cv2.VideoCapture(self.deviceId, cv2.CAP_DSHOW)
        except Exception as e:
            log(f"could not connect with cam {self.name}")
            self.handle = None

        try:
            for i in range(initialReads):
                self.success, self.image = self.handle.read()
            self.grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            if cv2.countNonZero(self.grayImage) == 0:
                log(f"captured image is black only, replugging the cam might help")
                self.releaseHandle()
                return None

        except Exception as e:
            log(f"could not capture frames")
            self.releaseHandle()


    def releaseHandle(self):
        if self.handle is not None:
            try:
                self.handle.release()
                self.handle = None
            except Exception as e:
                log(f"could not release handle {e}")
                self.handle = None


    def getResolution(self):
        return self.cols, self.rows


    def takeImage(self, show=False):

        if self.handle is None:
            log(f"{self.name} not available")
            return None

        #_, _ = self.handle.read()
        self.success, self.image = self.handle.read()

        if self.success:
            #log(f"{self.name} image successfully taken")

            # check for a complete black image (USB cam might not return a valid picture, replug cam)
            self.grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            if cv2.countNonZero(self.grayImage) == 0:
                log(f"captured image is black only, replugging the cam might help")
                return None

            if self.rotate != 0:
                self.image = imutils.rotate_bound(self.image, self.rotate)

            if show:
                cv2.imshow(f"usb image device {self.name}, deviceId: {self.deviceId}", self.image)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

            return self.image
        else:
            log(f"{self.name} failed to capture image")
            self.handle.release()
            self.handle = None


class D415Camera(Camera):

    # class variables, access as D415Camera.<variable>
    handle = None
    D415config = None
    streaming = False

    def __init__(self, name, deviceId, cols, rows, fovH, fovV, rotate, numReads):
        super().__init__(name, deviceId, cols, rows, fovH, fovV, rotate, numReads)

        # Configure depth and color streams
        if D415Camera.handle is None:
            try:
                D415Camera.handle = rs.pipeline()
                D415Camera.D415config = rs.config()
                D415Camera.D415config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
                D415Camera.D415config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
                log(f"{name} ready to stream")

            except Exception as e:
                log(f"could not initialize D415 cam, {e}")
                return

        if not D415Camera.streaming:
            self.startStream()

        if D415Camera.streaming:
            frames = D415Camera.handle.wait_for_frames()

            for i in range(self.numReads):
                rgb_frame = frames.get_color_frame()

            self.stopStream()


    def startStream(self):
        if not D415Camera.streaming:
            try:
                D415Camera.handle.start(D415Camera.D415config)
                D415Camera.streaming = True
                log(f"start D415 stream successful")

            except Exception as e:
                log(f"not able to start D415 stream: {e}")
                D415Camera.handle = None


    def stopStream(self):
        if D415Camera.streaming:
            D415Camera.handle.stop()
        D415Camera.streaming = False


    def takeImage(self, show=False):

        if not D415Camera.streaming:
            D415Camera.startStream()

        if not D415Camera.streaming:
            return None

        frames = D415Camera.handle.wait_for_frames()

        for i in range(self.numReads):
            colorFrame = frames.get_color_frame()

        if colorFrame is None:
            log(f"could not acquire rgb image from D415")
            colorImage = None
        else:
            colorImage = np.asanyarray(colorFrame.get_data())
            if show:
                cv2.imshow(f"D415 rgb", colorImage)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        return colorImage


    def takeDepth(self, show=False):

        if not D415Camera.streaming:
            D415Camera.startStream()

        if not D415Camera.streaming:
            return None

        decimate = rs.decimation_filter()
        decimate.set_option(rs.option.filter_magnitude, 3)

        frames = D415Camera.handle.wait_for_frames()

        depthFrame = frames.get_depth_frame()
        if depthFrame is None:
            log(f"could not acquire depth from D415")
            return None

        else:
            decimated = decimate.process(depthFrame)    # make 428x240x3 from 1280x720x3

            # Grab new intrinsics (may be changed by decimation)
            # depth_intrinsics = rs.video_stream_profile(depth_frame.profile).get_intrinsics()
            # w, h = depth_intrinsics.width, depth_intrinsics.height
            pc = rs.pointcloud()
            pointCloud = pc.calculate(decimated)

            # Pointcloud data to arrays
            verts = pointCloud.get_vertices()
            points = np.asanyarray(verts).view(np.float32).reshape(-1, 3)  # xzy [102720 <428x240>,3]

            if show:
                log(f"points available")

        return points


def savePointCloud(pc, filename):
    # save as pickle file for testing
    myFile = open(filename, 'wb')
    np.save(myFile, pc)
    myFile.close()


def loadPointCloud(filename):
    myFile = open(filename, 'rb')
    pc = np.load(myFile)
    myFile.close()
    return pc


def rotatePointCloud(verts, angle):

    # rotate over x-axis
    cosa = np.cos(np.radians(angle))
    sina = np.sin(np.radians(angle))

    # return rotated point cloud array
    return np.dot(verts, np.array([
        [1., 0, 0],
        [0, cosa, -sina],
        [0, sina, cosa]]))


def alignPointsWithGround(rawPoints, headPitch, imageAngle, camXYZ):
    '''
    raw points are taken in an angle
    rotate the point cloud to be aligned with the ground
    remove the ground and convert point height to above ground height
    raise below ground points to be an obstacle
    :return: aligned point cloud
    '''
    log(f"start align points with ground, headPitch: {headPitch:.0f}")

    # replace out of scope distance values with NaN
    with np.errstate(invalid='ignore'):
        rawPoints[:, 2][(rawPoints[:,2] < 0.2) |
                     (rawPoints[:,2] > 4)] = np.NaN

    #findObstacles.showSliceRaw(rawPoints, 208)

    # get image angle and cam xyz position
    #imageAngle, camXYZ = calculateCamXYZ(useHeadImu)

    #showPoints(points,     # rotate points for a horizontal representation of the points
    rotatedPoints = rotatePointCloud(rawPoints, -90-imageAngle)
    log(f"rotation angle: {-90-imageAngle:.1f}")

    ####################################################
    # after rotation:
    # points[0] = left/right, center=0
    # points[1] = horizontal distance to point, row 0 farthest
    # points[2] = height of point above ground, in relation to cam height
    ####################################################

    #showPoints(rotatedPoints, 'wall image rotated')

    # subtract the cam height from the points
    rotatedPoints[:,2] = rotatedPoints[:,2] - camXYZ[2]

    # set distance positive
    rotatedPoints[:,1] = -rotatedPoints[:,1]

    # show a rotated slice as line
    #findObstacles.showSlice(rotatedPoints, 208)

    # create obstacles for below ground points, suppress runtime warnings caused by nan values
    with np.errstate(invalid='ignore'):
        rotatedPoints[:,2] = np.where(rotatedPoints[:,2] < - 0.1, 1, rotatedPoints[:,2])

    return rotatedPoints        # for each col/row point the xyz values



def stopD415Stream():
    log(f"request stop streaming from D415")
    global D415streaming
    try:
        streamD415.stop()
        D415streaming = False
        return True
    except Exception as e:
        log(f"stop stream failed: {e}")
        D415streaming = False
        return False
