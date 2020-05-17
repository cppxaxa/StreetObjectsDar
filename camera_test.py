
import warnings  
warnings.catch_warnings()
warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=UserWarning)


# import threading
# import queue

# def fn1(data):
#     return 10 + data

# def fn2(data):
#     return 20 + data

# q = queue.Queue()

# t1 = threading.Thread(target=lambda qParam, dataParam: qParam.put(fn1(dataParam)), args=[q, 5])
# t2 = threading.Thread(target=lambda qParam, dataParam: qParam.put(fn2(dataParam)), args=[q, 5])

# t1.start()
# t2.start()

# t1.join()
# t2.join()

# while not q.empty():
#     el = q.get()
#     print(el)

# exit()





from lib.CameraAdapters import *
from lib.models.Frame import *
from lib.pydnet.infer import *

import cv2

import threading
import queue


import sys
sys.path.append("lib/tfSsdMobilenet")

from minimal_object_detection_lib import *

# Driver code

data = None
with open("StreetObjectsDarConfiguration.json") as f:
    data = f.read()
configuration = json.loads(data)

# pydCheckpoint = configuration["PyDnetConfiguration"]["Checkpoint"]
# pydWidth = configuration["PyDnetConfiguration"]["InputWidth"]
# pydHeight = configuration["PyDnetConfiguration"]["InputHeight"]

# pydModel = PyDNetInference(pydCheckpoint, pydWidth, pydHeight)

# ssdCheckpoint = configuration["TfSsdMobilenet"]["Checkpoint"]
# ssdLabelMap = configuration["TfSsdMobilenet"]["LabelMapPath"]
# ssdClassCount = configuration["TfSsdMobilenet"]["ClassCount"]


# objectDetector = MinimalObjectDetector(ssdCheckpoint, \
#                         ssdLabelMap, ssdClassCount)


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

        result = {}
        while not resultQueue.empty():
            el = resultQueue.get()
            if "Disparity" in el:
                result["Disparity"] = el["Disparity"]
            elif "LabelledBBox" in el:
                result["LabelledBBox"] = el["LabelledBBox"]
        return result

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



img = cv2.imread("image.jpg")

detector = CombinedDetector(configuration)
result = detector.Run(img)
print(result)

# a = time.perf_counter()
# disp = pydModel.Run(img)
# result = objectDetector.Process(img)
# b = time.perf_counter()
# print("Time", b - a)

# # a = time.perf_counter()
# # disp = pydModel.Run(img)
# # result = objectDetector.Process(img)
# # b = time.perf_counter()
# # print("Time", b - a)

# # a = time.perf_counter()
# # disp = pydModel.Run(img)
# # result = objectDetector.Process(img)
# # b = time.perf_counter()
# # print("Time", b - a)


# resultQueue = queue.Queue()
# threadList = []

# t1 = threading.Thread(target=lambda queueParam, frameParam: \
#     queueParam.put({"Disparity": pydModel.Run(frameParam)}), \
#         args=[resultQueue, img])
# threadList.append(t1)

# t2 = threading.Thread(target=lambda queueParam, frameParam: \
#     queueParam.put({"LabelledBBox": objectDetector.Process(frameParam)}), \
#         args=[resultQueue, img])
# threadList.append(t2)

# a = time.perf_counter()
# for t in threadList:
#     t.start()

# for t in threadList:
#     t.join()
# b = time.perf_counter()

# print("Time", b - a)

# while not resultQueue.empty():
#     el = resultQueue.get()
#     if "Disparity" in el:
#         cv2.imshow('', el["Disparity"])
#         cv2.waitKey(3000)
#         cv2.destroyAllWindows()

# # print(json.dumps(result))
