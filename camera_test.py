


from lib.CameraAdapters import *
from lib.models.Frame import *

# Driver code

data = None
with open("StreetObjectsDarConfiguration.json") as f:
    data = f.read()

config = json.loads(data)["CameraReaderConfiguration"]

cameraList = []

for camConf in config:
    print(camConf)
    camera = CreateCameraObject(camConf)
    cameraList.append(camera)

for i in range(1):
    for cam in cameraList:
        img = cam.grabThrottled()
        print(img)
    print("Iter", i)

cv2.imshow('', img)
cv2.waitKey()

