
from lib.CameraReaderNode import *
from lib.FramesDropperNode import *
from lib.InferenceGeneratorNode import *
from lib.CollatorNode import *
from lib.DistanceCalculatorNode import *

import json
from lib.pyPiper.pyPiper import Pipeline

def CreateStreetObjectsDarPipeline(callbackNode, threads=1, quiet=False):
    configurationFilename = "StreetObjectsDarConfiguration.json"
    configurationObject = None
    with open(configurationFilename) as f:
        configurationObject = json.loads(f.read())
    
    cameraReaderNode = CameraReaderNode("CameraReaderNode", \
        configurationObject = configurationObject)
    framesDropperNode = FramesDropperNode("FramesDropperNode", \
        configurationFilename = configurationFilename)
    inferenceGeneratorNode = InferenceGeneratorNode("InferenceGeneratorNode", \
        configurationObject = configurationObject)
    collatorNode = CollatorNode("CollatorNode", \
        configurationObject = configurationObject)
    distanceCalculatorNode = DistanceCalculatorNode("DistanceCalculator", \
        configurationObject = configurationObject)

    pipeline = None
    if callbackNode is None:
        print("CreateStreetObjectsDarPipeline callback not provided")
        pipeline = Pipeline(cameraReaderNode | \
            framesDropperNode | \
                inferenceGeneratorNode | \
                    collatorNode | \
                        distanceCalculatorNode, \
                            n_threads=threads, quiet=quiet)
    else:
        pipeline = Pipeline(cameraReaderNode | \
            framesDropperNode | \
                inferenceGeneratorNode | \
                    collatorNode | \
                        distanceCalculatorNode | \
                            callbackNode, \
                                n_threads=threads, quiet=quiet)
    return pipeline

class PipelineFactory:
    @staticmethod
    def CreatePipeline(type, callbackNode, threads=2, quiet=False):
        if type == "StreetObjectsDar":
            return CreateStreetObjectsDarPipeline(callbackNode, threads, quiet)
        else:
            print("PipelineFactory::CreatePipeline, type = {} invalid".format(type))
            return None