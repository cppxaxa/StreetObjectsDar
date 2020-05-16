
from lib.pyPiper.pyPiper import Node

class CameraReaderNode(Node):
    def setup(self, configurationObject):
        self.size = 1
        self.pos = 0
        self.configurationObject = configurationObject

    def run(self, data):
        self.close()
        