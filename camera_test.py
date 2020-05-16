


from lib.CameraAdapters import *
from lib.models.Frame import *
from lib.pydnet.infer import *

import cv2


import sys
sys.path.append("lib/tfSsdMobilenet")

from minimal_object_detection_lib import *

# Driver code

data = None
with open("StreetObjectsDarConfiguration.json") as f:
    data = f.read()

checkpoint = json.loads(data)["PyDnetConfiguration"]["Checkpoint"]
width = json.loads(data)["PyDnetConfiguration"]["InputWidth"]
height = json.loads(data)["PyDnetConfiguration"]["InputHeight"]

pydModel = PyDNetInference(checkpoint, width, height)

objectDetector = MinimalObjectDetector('lib/tfSsdMobilenet/object_detection/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', \
                        'lib/tfSsdMobilenet/object_detection/data/mscoco_label_map.pbtxt', 90)

img = cv2.imread("image.jpg")
disp = pydModel.Run(img)

cv2.imshow('', disp)
cv2.waitKey(3000)
cv2.destroyAllWindows()


result = objectDetector.Process(img)

print(json.dumps(result))
