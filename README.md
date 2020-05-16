# StreetObjectsDar

Street objects detection and ranging on a road traffic, esp. based on camera feed at a car or pedestrian view

# Architecture

[CameraReader] -> [FramesDropper/Filter] -> [Models for inference array] -> [Collator] -> [DistanceCalculator]

# Abbreviations

### CameraReader
- Reads from various image sources - static image, IpCamera, AndroidIPWebcam, Webcam

### FramesDropper/Filter - tightly coupled with CameraReader for performance
- Drops the extra frames and does the filtering if required (as of now, no filtering)

### Models for inference array
- PyDnet and TfSsdMobileNet should be enough to run on CPU for inference

### Collator
- Combines the async results from the models

### DistanceCalculator
- For every labelled object under the bounding box, take values from pydnet output and calculate a mean/median value representing distance from camera

# Development Tasks
- Define the pipeline with PyPiper with dummy modules
- Test the performance
- Develop the frames dropper and dummy CameraReader
- Set tuning parameters for the frames dropper e.g. time gap between frames, IsOldFramesAllowed
- Output from CameraFeed -> Frame
- Output from FramesDropper -> Frame
- Output from PyDnet -> InferredData(Frame, Type=pydnet, Disparity, LabelledBBox=None)
- Output from TfSsdMobileNet -> InferredData(Type=tfssdmobilenet, Disparity=None, LabelledBBox)
- Output Collator maintains a hashmap[camId][imageId] => {IsDisparityMatrixAvailabel, IsLabelledBBoxAvailabel} and if both conditions are met, publish the result as CollatedData
- Output from DistanceCalculator -> LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])

## Data Models
- Frame(camId, timestamp, imageId=Random, frame)
- Disparity(Matrix)
- LabelledBBox([{BBox, Label}, ...])
- InferredData(Frame, Type, Disparity, LabelledBBox)
- CollatedData(Frame, Disparity, LabelledBBox)
- LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])

# Progress
[ ] Define the pipeline with PyPiper with dummy modules
[ ] Test the performance
- [ ] Develop the frames dropper and dummy CameraReader
- [ ] Set tuning parameters for the frames dropper e.g. time gap between frames, IsOldFramesAllowed
- [ ] Output from CameraFeed -> Frame
- [ ] Output from FramesDropper -> Frame
- [ ] Output from PyDnet -> InferredData(Frame, Type=pydnet, Disparity, LabelledBBox=None)
- [ ] Output from TfSsdMobileNet -> InferredData(Type=tfssdmobilenet, Disparity=None, LabelledBBox)
- [ ] Output Collator maintains a hashmap[camId][imageId] => {IsDisparityMatrixAvailabel, IsLabelledBBoxAvailabel} and if both conditions are met, publish the result as CollatedData
- [ ] Output from DistanceCalculator -> LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])

- [ ] Frame(camId, timestamp, imageId=Random, frame)
- [ ] Disparity(Matrix)
- [ ] LabelledBBox([{BBox, Label}, ...])
- [ ] InferredData(Frame, Type, Disparity, LabelledBBox)
- [ ] CollatedData(Frame, Disparity, LabelledBBox)
- [ ] LabelledBBoxWithDistance([{BBox, Label, Distance}, ...])
