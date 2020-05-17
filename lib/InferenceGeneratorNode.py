
from lib.pyPiper.pyPiper import Node

from lib.pydnet.infer import *

import cv2

import threading
import queue


import sys
sys.path.append("lib/tfSsdMobilenet")

from minimal_object_detection_lib import *


class InferenceGeneratorNode(Node):
    def setup(self, configurationObject):
        self.configurationObject = configurationObject
        
        

    def run(self, data):
        self.emit(data)

        