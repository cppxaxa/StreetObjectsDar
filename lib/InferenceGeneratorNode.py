

import cv2

import threading
import queue
import multiprocessing

import sys
sys.path.append("lib/tfSsdMobilenet")

from lib.pyPiper.pyPiper import Node
from lib.pydnet.infer import *
from minimal_object_detection_lib import *

from lib.models.InferredData import *


class CombinedDetector:
    def __init__(self, configurationObject):
        self.configurationObject = configurationObject
        self.Initialize()
    
    def Run(self, image):
        resultQueue = queue.Queue()

        t1 = threading.Thread(target=lambda queueParam, frameParam: \
            queueParam.put({"Disparity": self.pydModel.Run(frameParam)}), \
                args=[resultQueue, image])

        t2 = threading.Thread(target=lambda queueParam, frameParam: \
            queueParam.put({"LabelledBBox": self.objectDetector.Process(frameParam)}), \
                args=[resultQueue, image])
        
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        disparity = None
        labelledBBox = None
        while not resultQueue.empty():
            el = resultQueue.get()
            if "Disparity" in el:
                disparity = el["Disparity"]
            elif "LabelledBBox" in el:
                labelledBBox = el["LabelledBBox"]
        return disparity, labelledBBox

    def Initialize(self):
        configuration = self.configurationObject
        pydCheckpoint = configuration["PyDnetConfiguration"]["Checkpoint"]
        pydWidth = configuration["PyDnetConfiguration"]["InputWidth"]
        pydHeight = configuration["PyDnetConfiguration"]["InputHeight"]

        self.pydModel = PyDNetInference(pydCheckpoint, pydWidth, pydHeight)

        ssdCheckpoint = configuration["TfSsdMobilenet"]["Checkpoint"]
        ssdLabelMap = configuration["TfSsdMobilenet"]["LabelMapPath"]
        ssdClassCount = configuration["TfSsdMobilenet"]["ClassCount"]
        
        self.objectDetector = MinimalObjectDetector(ssdCheckpoint, \
                        ssdLabelMap, ssdClassCount)



class InferenceGeneratorNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject
        self.detectorMap = {}

    def run(self, data):
        detector = self.getDetector()
        disparity, labelledBBox = detector.Run(data.frame)
        self.emit(InferredData(data, disparity, labelledBBox))

    def getDetector(self):
        pid = multiprocessing.current_process().pid
        if pid not in self.detectorMap:
            self.detectorMap[pid] = self.createDetectors()
        return self.detectorMap[pid]

    def createDetectors(self):
        return CombinedDetector(self.configurationObject)

        