# This program will counting people who enter or leave space
# I use caffe deep learning framework 
# https://caffe.berkeleyvision.org/
# https://www.pyimagesearch.com/2017/09/11/object-detection-with-deep-learning-and-opencv/
# MobileNet SSD
#


# Usage 
#python peopleCounter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --ip 0.0.0.0 --port 8000

from tracker.centroidtracker import CentroidTracker
from tracker.trackableobject import TrackableObject
from imutils.video import VideoStream 
from imutils.video import FPS
from flask import Response
from flask import Flask
from flask import render_template
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import threading


# initiation output frame 
outputFrame = None
lock = threading.Lock()

# initiation Flask program
app =Flask(__name__)

# with from input argument src=1 if secound cam on usb
vs = VideoStream(src=0).start()

#else in use on raspberry PI
#vs = VideoStream(usePiCamera=True).start()

#start the FPS counter
fps = FPS().start()

# waiting for cam
time.sleep(2.0)    

# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

# initialize the frame dimensions (we'll set them as soon as we read
# the first frame from the video)
W = None
H = None

# instantiate our centroid tracker, then initialize a list to store
# each of our dlib correlation trackers, followed by a dictionary to
# map each unique object ID to a TrackableObject
ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
trackers = []
trackableObjects = {}

# initialize the total number of frames processed thus far, along
# with the total number of objects that have moved either up or down
totalFrames = 0
totalDown = 0
totalUp = 0


def count_people():
    global vs, outputFrame, lock, W, H, totalUp,totalFrames,totalDown

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    while True:
        # read next frame from cam stream
        frame = vs.read()
        frame = imutils.resize(frame, width=400, height=300)
        # convert the input frame from BGR to grayscale to face detection
        # and convert BGR to RGB for face recognition
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # implementation value of empty H&W frame resources
        if W is None or H is None:
            (H, W) =frame.shape[:2]
        
        # initialize the table of box rectangles returned by object detector or trackers
        status = "WAITING"
        rects = []

        if totalFrames % args["skip_frames"] == 0:
            status = "DETECTING"
            trackers = []

            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()

            #loop over the detections
            for i in np.arange(0, detections.shape[2]):

                # probability of detection object 
                confidence = detections[0, 0, i, 2]
                
                # confidence must be biger than  
                if confidence > args["confidence"]:

                    # take index of class object from detection list
                    idx= int(detections[0, 0, i, 1])

                    if CLASSES[idx] != "person":
                        continue

                    # compute the coordinate od object box like int
                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")

                    # draw a dlib rectangle box and start dlib correlation tracker
                    tracker =dlib.correlation_tracker()
                    rect = dlib.rectangle(startX,startY,endX,endY)
                    tracker.start_track(rgb, rect)

                    # add tracker to list of trackers
                    trackers.append(tracker) 
        
        else :

            # loop over the trackers
            for tracker in trackers:
                # set status
                status = "TRACKING"

                # get the updated position and unpack coordination 
                tracker.update(rgb)
                pos = tracker.get_position()
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                # coordinates to rectangle boxes
                rects.append((startX,startY,endX,endY))
        
        # draw a horizontal line 
        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 255, 255), 2)
        # or if will be not horizontal
        # cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 255, 255), 2)

        # use centroid tracker to associate old objects centroids with new computed object centroids
        objects = ct.update(rects)

        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            
            # check to see if a trackable object exists for the current object ID
            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)
            
            # when it is none we can use this object to determine direction
            else :

                # the difference between the y-coordinate of the *current*
			    # centroid and the mean of *previous* centroids will tell
			    # us in which direction the object is moving (negative for
			    # 'up' and positive for 'down')
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                if not to.counted:
                    # if the direction is negative (indicating the object
				    # is moving up) AND the centroid is above the center
				    # line, count the object
                    if direction < 0 and centroid[1] < H // 2:
                        totalUp += 1
                        to.counted = True

				    # if the direction is positive (indicating the object
				    # is moving down) AND the centroid is below the
				    # center line, count the object
                    elif direction > 0 and centroid[1] > H//2 :
                        totalDown +=1
                        to.counted = True
            
            # store trackable object in our dictionary
            trackableObjects[objectID] = to

            # draw both the ID of the object and the centroid
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        # prepare the informtion, which will be writed on frame
        info = [
		    ("Entries", totalUp),
		    ("Outgoing", totalDown),
            ("PeopleIn", totalUp-totalDown),
		    ("Status", status),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # increment the total number of frames processed thus far and
	    # then update the FPS counter
        totalFrames += 1
        fps.update()
        with lock:
            outputFrame = frame.copy()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    #end function

def generate(): 
    global outputFrame, lock

    # loop under output stream
    while True:
        # wait for lock(zatrzymanie akcji do czasu 'otrzymania' locka )
        with lock:
            if outputFrame is None:
                continue
            # encoded frame in form JPEG 
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # 
            if not flag:
                continue

        # return frame like byte array jpeg
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route("/video3")
def video():
    # return response (MIME type)
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
        # create the parser of intput arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prototxt", required=True,help="path to Caffe 'deploy' prototxt file")
    parser.add_argument("-m", "--model", required=True,help="path to Caffe pre-trained model")
    parser.add_argument("-i", "--ip", type=str, required=True, help="ip address of device")
    parser.add_argument("-o", "--port", type=int, required=True,help="server port number (1024 to 65535) ")
    parser.add_argument("-c", "--confidence", type=float, default=0.4,help="minimum propability to classify object")
    parser.add_argument("-s", "--skip-frames", type=int, default=30,help="# of skip frames between detections")
    args = vars(parser.parse_args())

    t = threading.Thread(target=count_people)
    t.daemon = True
    t.start()
    # run flask app
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
vs.stop()