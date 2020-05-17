
import warnings  
warnings.catch_warnings()
warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=UserWarning)
warnings.filterwarnings("ignore",category=Warning)

from lib.PipelineFactory import *

class CustomCallbackNode(Node):
    def run(self, data):
        print(data.LabelledBBox)

if __name__ == '__main__':
    customCallbackNode = CustomCallbackNode("endpoint")
    pipeline = PipelineFactory.CreatePipeline(callbackNode=customCallbackNode, \
        type="StreetObjectsDar")
    pipeline.run()
    
