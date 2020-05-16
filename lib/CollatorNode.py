
from lib.pyPiper.pyPiper import Node

class CollatorNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject

    def run(self, data):
        self.emit(data)

        