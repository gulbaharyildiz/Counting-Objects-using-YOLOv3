# Counting Objects using YOLOv3
YOLO is a pretrained network to detect 80 objectsfrom an image as mentioned in the.txt file.

# Files required for yolo
yolov3.txt - Contains the name of 80 objects

yolov3-tiny.cfg - contains the values of different layers like batch size, filters and more

yolov3.weights - Pretrained Model

Download the pre-trained YOLO v3-tiny weights file from this 

**Command format** 
 _$ python yolo_opencv.py --image /path/to/input/image --config /path/to/config/file --weights /path/to/weights/file --classes /path/to/classes/file_
