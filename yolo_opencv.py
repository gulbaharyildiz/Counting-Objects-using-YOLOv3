import cv2
import argparse
import numpy as np
import os
from time import sleep
os.system('fswebcam -r 640x480 --no-banner image.jpg')
sleep(2)
cv2.imread('image.jpg')
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = cv2.imread('image.jpg'))
ap.add_argument('-c', '--config', required=True,
                help = '/home/pi/Desktop/Counting-Objects-using-YOLOv3/yolov3.cfg')
ap.add_argument('-w', '--weights', required=True,
                help = '/home/pi/Desktop/Counting-Objects-using-YOLOv3/yolov3-tiny.weights')
ap.add_argument('-cl', '--classes', required=True,
                help = '/home/pi/Desktop/Counting-Objects-using-YOLOv3/yolov3.txt')
args = ap.parse_args()


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])
    
    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-4,y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


image = cv2.imread(args.image)

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392
#image = cv2.imread(args["image"])
#(Height,Width) = image.shape[:2]
#print("width: {} pixels".format(Width))
#print("Height: {}  pixels".format(Height))
classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet(args.weights, args.config)

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.4
nms_threshold = 0.3

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.4:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
print(len(class_ids))
print(class_ids)
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
print("Indices is ")
count=0
for i in indices:
    i = i[0]
    count+=1
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
print('apple count:',count)
cv2.imshow("object detection", image)
cv2.waitKey()
    
cv2.imwrite("O_apple.jpg", image)
cv2.destroyAllWindows()
