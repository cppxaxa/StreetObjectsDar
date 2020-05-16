
from lib.pyPiper.pyPiper import Node

class CallbackNode(Node):
    def run(self, data):
        self.emit(data)

        