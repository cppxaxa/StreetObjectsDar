
import warnings  
warnings.catch_warnings()
warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=UserWarning)
warnings.filterwarnings("ignore",category=Warning)

from lib.PipelineFactory import *
from lib.ResultsGeneratorFactory import *

import cv2
import random

def DrawBBoxWithLabelledBBox(img, sourceShape, bboxList):
    targetShape = img.shape
    multiplierW = targetShape[0] / sourceShape[0]
    multiplierH = targetShape[1] / sourceShape[1]
    for bbox in bboxList:
        start = (int(bbox['x'] * multiplierW), 
                    int(bbox['y'] * multiplierH))
        end = (int((bbox['x'] + bbox['w']) * multiplierW), 
                    int((bbox['y'] + bbox['h']) * multiplierH))
        color = (0, 255, 0)
        thickness = 1
        labelRequired = False
        if bbox['distance'] < 0.85:
            color = (255, 0, 0)
        if bbox['distance'] < 0.58:
            color = (0, 0, 255)
            thickness = 2
            labelRequired = True
        img = cv2.rectangle(img, start, end, color, thickness)
        if labelRequired:
            img = cv2.putText(img, bbox['label'] + "," + str(bbox['confidence']), \
                (start[0] + 5, start[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, \
                    0.5, color, 1, cv2.LINE_AA)


class CustomCallbackNode(Node):
    def run(self, data):
        print(data)
        id = random.randint(100, 10000)
        
        img = data.Disparity.copy()
        frame = data.Frame.frame.copy()
        sourceShape = data.Frame.frame.shape
        DrawBBoxWithLabelledBBox(img, sourceShape, data.BBoxList)
        DrawBBoxWithLabelledBBox(frame, sourceShape, data.BBoxList)

        cv2.imshow(str(id), img)
        cv2.imshow(str(id + 1), frame)
        cv2.waitKey()
        cv2.destroyWindow(str(id))
        cv2.destroyWindow(str(id + 1))

if __name__ == '__main__':
    customCallbackNode = CustomCallbackNode("endpoint")

    resultsPublisherNode = ResultsFormatterFactory.CreateResultsFormatter(customCallbackNode)
    # print(resultsPublisherNode)

    pipeline = PipelineFactory.CreatePipeline(callbackNode=resultsPublisherNode, \
        type="StreetObjectsDar")
    pipeline.run()
    
