
from lib.pyPiper.pyPiper import Node

class FramesDropperNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject

    def run(self, data):
        self.emit(data)

        