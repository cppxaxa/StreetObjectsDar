

class InferredData:
    def __init__(self, frame = None, disparity = None, labelledBBox = None):
        self.Frame = frame
        self.Disparity = disparity
        self.LabelledBBox = labelledBBox
    
    def __str__(self):
        return "InferredData/Disparity={}/LabelledBBox={}/Frame={}"\
            .format(self.Disparity is not None, \
                self.LabelledBBox is not None, self.Frame)
                