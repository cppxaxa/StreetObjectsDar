

from lib.PipelineFactory import *

class CustomCallbackNode(Node):
    def run(self, data):
        print(data)

if __name__ == '__main__':
    customCallbackNode = CustomCallbackNode("endpoint")
    pipeline = PipelineFactory.CreatePipeline(callbackNode=customCallbackNode, \
        type="StreetObjectsDar", threads=2, quiet=True)
    pipeline.run()

