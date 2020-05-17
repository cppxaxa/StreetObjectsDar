

class LabelledBBoxWithDistance:
    def __init__(self, Frame = None, Disparity = None, BBoxList = None):
        self.Frame = Frame
        self.Disparity = Disparity
        self.BBoxList = BBoxList
    
    def __str__(self):
        return "LabelledBBoxWithDistance/Frame={}/Disparity={}/BBoxList={}"\
            .format(self.Frame is not None, self.Disparity is not None, \
                self.BBoxList is not None)
                