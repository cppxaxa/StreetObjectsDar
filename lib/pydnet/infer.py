#
# MIT License
#
# Copyright (c) 2018 Matteo Poggi m.poggi@unibo.it
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import tensorflow as tf
import os
from lib.pydnet.utils import *
from lib.pydnet.pydnet import *

# forces tensorflow to run on CPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

class PyDNetInference:
  def __init__(self, checkpointPath, width, height):
    self.width = width
    self.height = height
    self.checkpointPath = checkpointPath
    self.Initialize()
    
  def Initialize(self):
    self.graph = tf.Graph()
    self.placeholders = {'im0':tf.placeholder(tf.float32,[None, None, None, 3], name='im0')}
    with tf.variable_scope("model") as scope:
      self.model = pydnet(self.placeholders)
    self.init = tf.group(tf.global_variables_initializer(), \
                    tf.local_variables_initializer())
    self.loader = tf.train.Saver()
    self.sess = tf.Session()
    self.sess.run(self.init)
    self.loader.restore(self.sess, self.checkpointPath)

  def Run(self, image):
    img = image
    img = cv2.resize(img, (self.width, self.height)).astype(np.float32) / 255.
    img = np.expand_dims(img, 0)
    disp = self.sess.run(self.model.results[0], feed_dict={self.placeholders['im0']: img})

    disp_color = applyColorMap(disp[0,:,:,0]*20, 'gray')
    return disp_color







# if __name__ == '__main__':
#   model = PyDNetInference('lib/pydnet/checkpoint/IROS18/pydnet', 640, 448)
  
#   img = cv2.imread("1.jpg")
#   result = model.Run(img)
  
#   cv2.imshow('', result)
#   cv2.waitKey()
