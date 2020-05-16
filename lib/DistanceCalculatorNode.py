
from lib.pyPiper.pyPiper import Node

class DistanceCalculatorNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject

    def run(self, data):
        self.emit(data)

        