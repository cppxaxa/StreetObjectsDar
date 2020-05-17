
from lib.pyPiper.pyPiper import Node
from lib.models.LabelledBBoxWithDistance import *

def CalculateBBoxDistance(disparity, sourceShape, bboxList):
    targetShape = disparity.shape
    multiplierW = targetShape[0] / sourceShape[0]
    multiplierH = targetShape[1] / sourceShape[1]
    bboxWithDistance = []
    for bbox in bboxList:
        x = min(bbox['topleft']['x'], bbox['bottomright']['x'])
        y = min(bbox['topleft']['y'], bbox['bottomright']['y'])
        w = max(bbox['topleft']['x'], bbox['bottomright']['x']) - x
        h = max(bbox['topleft']['y'], bbox['bottomright']['y']) - y
        nx = int(x * multiplierW)
        ny = int(y * multiplierH)
        nw = int(w * multiplierW)
        nh = int(h * multiplierH)
        croppedDisparity = disparity[nx: nx + nw, ny: ny + nh]
        label = bbox['label']
        confidence = bbox['confidence']
        distance = croppedDisparity.mean()
        bboxWithDistance.append({"x": x, "y": y, "w": w, "h": h, \
            "label": label, "confidence": confidence, \
                "distance": distance})
    return bboxWithDistance

class DistanceCalculatorNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject

    def run(self, data):
        bboxWithDistance = CalculateBBoxDistance(data.Disparity, data.Frame.frame.shape, data.LabelledBBox)
        result = LabelledBBoxWithDistance(data.Frame, data.Disparity, bboxWithDistance)
        self.emit(result)

        