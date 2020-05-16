
import json
from lib.pyPiper.pyPiper import Node

class FramesDropperNode(Node):
    def setup(self, configurationFilename):
        self.configurationFilename = configurationFilename
        self.dropOnePerCount = 0
        self.refreshConfiguration()
        self.hashMap = {}

    def run(self, data):
        if self.validate(data):
            self.emit(data)

    def validate(self, frame):
        if self.dropOnePerCount > 1:
            if frame.camId in self.hashMap:
                self.hashMap[frame.camId] += 1
            else:
                self.hashMap[frame.camId] = 1

            if self.hashMap[frame.camId] >= self.dropOnePerCount:
                self.hashMap[frame.camId] = 0
                return False
        return True


    def refreshConfiguration(self):
        with open(self.configurationFilename) as f:
            configuration = json.loads(f.read())["FramesDropperConfiguration"]
        self.dropOnePerCount = configuration["DropOnePerCount"]
        