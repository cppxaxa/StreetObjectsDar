
import json

from lib.pyPiper.pyPiper import Node

import multiprocessing
from socketIO_client import SocketIO, BaseNamespace

### Problems
# Unused callbackNode/ Improper way
# ResultsFormatterFactory should generate a composite
#   results formatters object (array) based on config

class ResultsPublisherV1Namespace(BaseNamespace):
    def on_my_response(self, *args):
        # print('my_response', args)
        pass

class StreetObjectsDarResultsV1Node(Node):
    def setup(self, callbackNode, configurationFilename):
        self.callbackNode = callbackNode
        self.configurationFilename = configurationFilename

        self.configurationObject = None
        with open(configurationFilename) as f:
            self.configurationObject = json.loads(f.read())
        self.serverConfig = self.configurationObject["ServerConfiguration"]

        self.clientMap = {}

    def run(self, data):
        transformedData = self.dataTransformer(data)

        self.getNamespace().emit('room_event',
            {
                'data': transformedData, 
                'receive_count': 0, 
                'room': 'StreetObjectsDarResultsV1'
            })

        if self.callbackNode is not None:
            self.callbackNode.run(data)
        self.emit(data)

    def getNamespace(self):
        pid = multiprocessing.current_process().pid
        if pid not in self.clientMap:
            self.clientMap[pid] = self.createSocketClient()
        return self.clientMap[pid]

    def createSocketClient(self):
        socketIO = SocketIO(self.serverConfig["Host"], self.serverConfig["Port"])
        resultsNamespace = socketIO.define(ResultsPublisherV1Namespace, '/result')

        print('Host', self.serverConfig["Host"])
        print('Port', self.serverConfig["Port"])
        print("Socket created", socketIO, "for pid", multiprocessing.current_process().pid)

        return resultsNamespace

    def dataTransformer(self, data):
        tBbox = []
        filterLabel = set(self.configurationObject["StreetObjectsDarResultsV1"] \
            ["SupportedLabels"])
        for el in data.BBoxList:
            if el["label"] not in filterLabel: continue
            tBbox.append({
                "x": el["x"],
                "w": el["w"],
                "d": str(el["distance"]),
                "label": el["label"]
            })
        return {
            "width": data.Frame.frame.shape[0],
            "height": data.Frame.frame.shape[1],
            "cameraFovAngle": self.configurationObject["StreetObjectsDarResultsV1"] \
                ["CameraMetadata"][data.Frame.camId - 1]["CameraFovAngle"],
            "bboxList": tBbox
        }


class ResultsFormatterFactory:
    @staticmethod
    def CreateResultsFormatter(callbackNode):
        # Load configuration
        configurationFilename = "StreetObjectsDarConfiguration.json"
        configurationObject = None
        with open(configurationFilename) as f:
            configurationObject = json.loads(f.read())
        resultConfiguration = configurationObject["ResultConfiguration"]

        # Generate the callback function
        if resultConfiguration["StreetObjectsDarResultsV1"]:
            return StreetObjectsDarResultsV1Node('results', callbackNode=callbackNode, \
                configurationFilename=configurationFilename)
        else:
            print("ResultsFormatterFactory::CreateResultsFormatter, invalid")
            return None