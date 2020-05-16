import random
import time

class Frame:
    def __init__(self, camId = None, frame = None, timestamp = None, imageId = None):
        self.camId = camId
        self.timestamp = timestamp
        self.imageId = imageId
        self.frame = frame

        if timestamp is None:
            self.timestamp = time.perf_counter()

        if imageId is None:
            self.imageId = random.randint(100, 10000)

    def __str__(self):
        return "Frame/cam" + str(self.camId) + "/" + \
            str(self.timestamp) + "/imgId" + str(self.imageId) + \
                "/" + str(self.frame.shape)
    
