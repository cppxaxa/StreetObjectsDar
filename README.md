# StreetObjectsDar

Street objects detection and ranging on a road traffic, esp. based on camera feed at a car or pedestrian view

# Architecture

[CameraReader] -> [FramesDropper/Filter] -> [Models for inference array] -> [DistanceCalculator] -> [Suggest Throttling Percentage] -> [Custom Callback]

# Abbreviations

### CameraReader
- Reads from various image sources - static image, IpCamera, AndroidIPWebcam, Webcam

### FramesDropper/Filter
- Drops the extra frames and does the filtering if required

### Models for inference array
- PyDnet and TfSsdMobileNet should be enough to run on CPU for inference

### DistanceCalculator
- For every labelled object under the bounding box, take values from pydnet output and calculate a mean/median value representing distance from camera

# Development Tasks
- Define the pipeline with PyPiper with dummy modules
- Test the performance
- Develop the frames dropper and dummy CameraReader
- Set tuning parameters for the frames dropper e.g. time gap between frames, IsOldFramesAllowed
- Output from CameraFeed -> Frame
- Output from FramesDropper -> Frame
- Output from PyDnet -> InferredData(Type=pydnet, Disparity, LabelledBBox=None)
- Output from TfSsdMobileNet -> InferredData(Type=tfssdmobilenet, Disparity=None, LabelledBBox)
- Output from DistanceCalculator -> LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])

## Data Models
- Frame(camId, timestamp, imageId=Random, frame)
- Disparity(Matrix)
- LabelledBBox([{BBox, Label}, ...])
- InferredData(Frame, Type, Disparity, LabelledBBox)
- LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])
- LabelledBBoxWithDistanceFps([{BBox, Label, Distance, Fps}, ...])

# Progress
- [x] Define the pipeline with PyPiper with dummy modules
- [x] Develop the frames dropper and dummy CameraReader
- [x] Test the performance
- [x] Set tuning parameters for the frames dropper e.g. time gap between frames, IsOldFramesAllowed
- [x] Output from CameraFeed -> Frame
- [x] Output from FramesDropper -> Frame
- [x] Output from PyDnet -> InferredData*(Type=pydnet, Disparity, LabelledBBox=None)
- [x] Output from TfSsdMobileNet -> InferredData*(Type=tfssdmobilenet, Disparity=None, LabelledBBox)
- [x] Collated data from both models
- [ ] Output from DistanceCalculator -> LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])
- [ ] Find the pipeline fps, suggest throttling

- [x] Frame(camId, frame, timestamp=Timestamp, imageId=Random)
- [x] Disparity(Matrix/GrayImage)
- [x] LabelledBBox([{bottomright, topleft, label, confidence}, ...])
- [x] InferredData(Frame, Type, Disparity, LabelledBBox)
- [ ] LabelledBBoxWithDistance(Frame, Type, Disparity, BBoxList=[{BBox, Distance}, ...])
- [ ] LabelledBBoxWithDistanceFps(Frame, Type, Disparity, Fps, BBoxList=[{BBox, Distance}, ...])
