
import cv2
import json
import time
import abc
import urllib.request
import numpy as np

class GrabMethods(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def grab(self):
        pass

    @abc.abstractmethod
    def grabThrottled(self):
        pass

    def grabByDrop(self, frameDrop=0):
        for _ in range(frameDrop):
            self.grab()
        return self.grab()
    
    def grabByDelay(self, delay=0):
        time.sleep(delay)
        return self.grab()


class SlideshowCamera(GrabMethods):
    def __init__(self, urlList, flipLeftRight, fps):
        self.urlList = urlList
        self.index = 0
        self.count = len(urlList)
        self.flipLeftRight = flipLeftRight
        self.fps = fps
        self.lastRequestTimestamp = time.perf_counter()
        self.timegap = 1/fps
    
    def grab(self):
        gap = self.timegap - (time.perf_counter() - self.lastRequestTimestamp)
        if gap > 0.010:
            time.sleep(gap)
        img = cv2.imread(self.urlList[self.index])
        self.index += 1
        if self.index >= self.count: self.index = 0
        if self.flipLeftRight:
            img = cv2.flip(img, 1)
        return img
    
    def grabThrottled(self):
        return self.grabByDelay(1/self.fps)

    def close(self):
        pass


class StaticImageCamera(GrabMethods):
    def __init__(self, url, flipLeftRight, fps=30):
        self.url = url
        self.fps = fps
        self.flipLeftRight = flipLeftRight
    
    def grab(self):
        img = cv2.imread(self.url)
        if self.flipLeftRight:
            img = cv2.flip(img, 1)
        return img
    
    def grabThrottled(self):
        return self.grabByDelay(1/self.fps)

    def close(self):
        pass


class StatefulWebcamCamera(GrabMethods):
    def __init__(self, webcamId, flipLeftRight, expectedFps=30):
        self.webcamId = webcamId
        self.expectedFps = expectedFps
        self.flipLeftRight = flipLeftRight

        self.lastGrab = time.perf_counter()
        self.cap = cv2.VideoCapture(webcamId)

        try:
            (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
            if int(major_ver)  < 3 :
                fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
            else :
                fps = self.cap.get(cv2.CAP_PROP_FPS)
            if fps != 0: self.expectedFps = expectedFps
        except:
            self.expectedFps = expectedFps

    def grab(self):
        diff = time.perf_counter() - self.lastGrab
        lim = int(diff * self.expectedFps) + 1
        for _ in range(lim):
            __, img = self.cap.read()
        self.lastGrab = time.perf_counter()
        if self.flipLeftRight:
            img = cv2.flip(img, 1)
        return img

    def grabThrottled(self):
        return self.grabByDrop(0)

    def close(self):
        del self.cap



class AndroidIpWebcam(GrabMethods):
    def __init__(self, shotUrl, flipLeftRight):
        self.shotUrl = shotUrl
        self.flipLeftRight = flipLeftRight
    
    def grab(self):
        imgResp = urllib.request.urlopen(self.shotUrl)
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img = cv2.imdecode(imgNp,-1)
        if self.flipLeftRight:
            img = cv2.flip(img, 1)
        return img
    
    def grabThrottled(self):
        return self.grab()

    def close(self):
        pass



def CreateCameraObject(configuration):
    type = configuration["Type"]
    flipLeftRight = configuration["FlipLeftRight"]

    camera = None

    if type == "StaticImage":
        url = configuration["Url"]
        camera = StaticImageCamera(url, flipLeftRight)
    elif type == "Webcam":
        webcamId = configuration["WebcamId"]
        camera = StatefulWebcamCamera(webcamId, flipLeftRight)
    elif type == "AndroidIpWebcam":
        shotUrl = configuration["ShotUrl"]
        camera = AndroidIpWebcam(shotUrl, flipLeftRight)
    elif type == "Slideshow":
        urlList = configuration["Sequence"]
        fps = configuration["Fps"]
        camera = SlideshowCamera(urlList, flipLeftRight, fps)
    else:
        print("Invalid camera configuration: {}".format(configuration))

    return camera

