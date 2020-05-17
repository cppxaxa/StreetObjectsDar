
from lib.pyPiper.pyPiper import Node
from lib.CameraAdapters import *
from lib.models.Frame import *

class CameraReaderNode(Node):
    def setup(self, configurationObject):
        self.size = 1
        self.pos = 0
        self.configurationObject = configurationObject

        config = configurationObject["CameraReaderConfiguration"]
        self.cameraList = []

        for camConf in config:
            camera = CreateCameraObject(camConf)
            self.cameraList.append(camera)


    def run(self, data):
        if len(self.cameraList) <= 0:
            self.close()

        for _ in range(1):
            id = 0
            for cam in self.cameraList:
                id += 1
                img = cam.grabThrottled()
                self.emit(Frame(id, img))
        
        self.close()
