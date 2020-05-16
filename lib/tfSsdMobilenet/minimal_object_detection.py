import os
import cv2
import numpy as np
import tensorflow as tf
import json
import re

from utils.app_utils import draw_boxes_and_labels
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    
    rect_points, class_names, class_colors = draw_boxes_and_labels(
        boxes=np.squeeze(boxes),
        classes=np.squeeze(classes).astype(np.int32),
        scores=np.squeeze(scores),
        category_index=category_index,
        min_score_thresh=.5)

    return image_np, rect_points, class_names, class_colors



class MinimalObjectDetector:
    def __init__(self):
        pass
    
    def Initialize(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            self.od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                self.serialized_graph = fid.read()
                self.od_graph_def.ParseFromString(self.serialized_graph)
                tf.import_graph_def(self.od_graph_def, name='')

            self.sess = tf.Session(graph=self.detection_graph)
    
    def Process(self, frame):
        output, rec_points, class_names, class_colors = detect_objects(frame, self.sess, self.detection_graph)
        height, width, _ = frame.shape
        result = []
        for point, name, color in zip(rec_points, class_names, class_colors):
            splitVal = name[0].split(':')
            label = splitVal[0]
            confidence = int(re.findall("\d+", name[0])[0]) / 100

            br_x = int(point['xmax'] * width)
            by_y = int(point['ymax'] * height)

            tl_x = int(point['xmin'] * width)
            tl_y = int(point['ymin'] * height)

            resultUnit = {
                "label": label,
                "bottomright":{
                    "y": by_y,
                    "x": br_x
                },
                "topleft":{
                    "y": tl_y,
                    "x": tl_x
                },
                "confidence": confidence
            }
            result.append(resultUnit)
        return result

    def Close(self):
        self.sess = None
        self.detection_graph = None
        self.serialized_graph = None
        self.od_graph_def = None



if __name__ == '__main__':
    # video_capture = WebcamVideoStream(0, width=480, height=360).start()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    objectDetector = MinimalObjectDetector()
    objectDetector.Initialize()

    while True:
        _, frame = cap.read()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        result = objectDetector.Process(frame_rgb)
        
        print(json.dumps(result))

        # output_rgb = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        # cv2.imshow('Video', output_rgb)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    video_capture.stop()
    cv2.destroyAllWindows()
