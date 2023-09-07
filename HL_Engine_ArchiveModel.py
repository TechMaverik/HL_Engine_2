import cv2
import csv
import time
import collections
import numpy as np
from HL_Engine_ArchiveModel_Tracer import *
from datetime import datetime

# Initialize Tracker
tracker = EuclideanDistTracker()
# Initialize the videocapture object
input_size = 320
# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2
font_color = (0, 0, 255)
font_size = 0.5
font_thickness = 2
# List for store vehicle count information
temp_up_list = []
temp_down_list = []
up_list = [0, 0, 0, 0]
down_list = [0, 0, 0, 0]
# Middle cross line position
# middle_line_position = 225   
# up_line_position = middle_line_position - 15
down_line_position = 500
# Store Coco Names in a list
classesFile = "coco.names"
classNames = open(classesFile).read().strip().split('\n')
# class index for our required detection classes
required_class_index = [2, 3, 5, 7]
detected_classNames = []
## Model Files
modelConfiguration = 'yolov3-320.cfg'
modelWeigheights = 'yolov3-320.weights'
# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)
# Configure the network backend
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')

# Function for finding the center of a rectangle
def calculate_cendroid(x, y, w, h):
    x1=int(w/2)
    y1=int(h/2)
    cx = x+x1
    cy=y+y1
    return cx, cy

# Function for count vehicle
def count_vehicle(box_id, img):
    x, y, w, h, id, index = box_id
    # Find the center of the rectangle for detection
    center = calculate_cendroid(x, y, w, h)
    ix, iy = center

    """Need to write logic here"""
    if iy > down_line_position:        
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        frequency = collections.Counter(detected_classNames) 
        if id not in down_list:
            down_list.append(id)
            with open("vehicle_count_classification.csv", 'a') as f1:
                cwriter = csv.writer(f1)
                cwriter.writerow([currentTime,"------>",frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
                

    # Draw circle in the middle of the rectangle
    cv2.circle(img, center, 2, (0, 0, 255), -1)  # end here
    print(len(down_list))

# Function for finding the detected objects from the network output
def operation(outputs,img):
    global detected_classNames 
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    # print(classIds)
    if len(indices)>0:
        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            # print(x,y,w,h)

            color = [int(c) for c in colors[classIds[i]]]
            name = classNames[classIds[i]]
            detected_classNames.append(name)
            # Draw classname and confidence score 
            cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])

        # Update the tracker for each object
        # boxes_ids = tracker.update(detection)
        # for box_id in boxes_ids:
        #     count_vehicle(box_id, img)


def detect_vehicles_from_video_stream(video_source):
    try:
        load_video = cv2.VideoCapture(video_source)
        while True:        
            success, img = load_video.read()
            img = cv2.resize(img,(0,0),None,0.5,0.5)
            ih, iw, channels = img.shape
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)
            # Set the input of the network
            net.setInput(blob)
            layersNames = net.getLayerNames()
            outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
            # Feed data to the network
            outputs = net.forward(outputNames)    
            # Find the objects from the network output
            operation(outputs,img)

            # Draw the crossing lines for reference
            # cv2.line(img, (middle_line_position, 0), (middle_line_position,iw ), (255, 0, 255), 2)
            # cv2.line(img, (0, up_line_position), (iw, up_line_position), (0, 0, 255), 2)
            cv2.line(img, (0, down_line_position), (iw, down_line_position), (0, 0, 255), 2)  
            
            # Show the frames
            cv2.imshow('IRIS Processed video', img)

            if cv2.waitKey(1) == ord('q'):
                break
        # Finally realese the capture object and destroy all active windows
        load_video.release()
        cv2.destroyAllWindows()
    except:
        print("Found an Exception --->Handled")



def detect_vehicles_from_image(image):
    img = cv2.imread(image)
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)
    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
    # Feed data to the network
    outputs = net.forward(outputNames)
    # Find the objects from the network output
    operation(outputs,img)
    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)   
    # cv2.imshow("IRIS Processed Image", img)
    # cv2.waitKey(0)
    # save the data to a csv file
    print("Processing --> "+str(image))
    with open("vehicle_count_classification_from_image.csv", 'a') as f1:
        currentDateAndTime = datetime.now()
        currentTime = currentDateAndTime.strftime("%H:%M:%S")
        cwriter = csv.writer(f1)
        cwriter.writerow([image, currentTime, "===>" ,frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    f1.close()
