
import json
from lib.pyPiper.pyPiper import Node
import time

class FramesDropperNode(Node):
    def setup(self, configurationFilename):
        self.configurationFilename = configurationFilename
        self.takeSpecifiedPercentageFrames = 100
        self.refreshConfiguration()
        self.hashMap = {}

        self.lastConfigRefreshed = time.perf_counter()

    def run(self, data):
        if time.perf_counter() - self.lastConfigRefreshed > 30:
            self.refreshConfiguration()
            self.lastConfigRefreshed = time.perf_counter()

        if self.validate(data):
            self.emit(data)

    def validate(self, frame):
        if self.takeSpecifiedPercentageFrames < 100:
            if frame.camId in self.hashMap:
                self.hashMap[frame.camId] += 1
            else:
                self.hashMap[frame.camId] = 1

            # given 25% means skip 3 frames and proceed with
            # 1 frame
            #
            # (100 // 25) - 1 = 3

            if self.hashMap[frame.camId] >= (100 // self.takeSpecifiedPercentageFrames):
                self.hashMap[frame.camId] = 0
                return True
            return False
        return True


    def refreshConfiguration(self):
        with open(self.configurationFilename) as f:
            configuration = json.loads(f.read())["FramesDropperConfiguration"]
        self.takeSpecifiedPercentageFrames = configuration["TakeSpecifiedPercentageFrames"]
        