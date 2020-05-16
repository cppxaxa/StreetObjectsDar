


from lib.CameraAdapters import *
from lib.models.Frame import *
from lib.pydnet.infer import *

import cv2

# Driver code

data = None
with open("StreetObjectsDarConfiguration.json") as f:
    data = f.read()

checkpoint = json.loads(data)["PyDnetConfiguration"]["Checkpoint"]
width = json.loads(data)["PyDnetConfiguration"]["InputWidth"]
height = json.loads(data)["PyDnetConfiguration"]["InputHeight"]

model = PyDNetInference(checkpoint, width, height)

img = cv2.imread("image.jpg")
disp = model.Run(img)

cv2.imshow('', disp)
cv2.waitKey()

