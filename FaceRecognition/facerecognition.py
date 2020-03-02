# Author Mikołaj Ambroziak
# facerecognition.py is a application that recognizes faces from input model (pickle file)
# in real time cam, and stream video live to the website 
# 
# Use this file in that way:
# python facerecognition.py --cascade cascade.xml --pickle encodings.pickle --ip 0.0.0.0 --port 8000

# all the necessery packages
from imutils.video import VideoStream 
from imutils.video import FPS
from flask import Response
from flask import Flask
from flask import render_template
import face_recognition
import threading
import argparse
import imutils
import pickle
import datetime
import time
import cv2

# initiation output frame 
outputFrame = None
lock = threading.Lock()

# initiation Flask program
app =Flask(__name__)

# with from input argument
vs = VideoStream(src=0).start()

#else in use on raspberry PI
#vs = VideoStream(usePiCamera=True).start()

#start the FPS counter
fps = FPS().start()

# waiting for cam
time.sleep(2.0)    


def detect_face():
    global vs, outputFrame, lock
    
    # loading input file ( OpenCV's Haar cascade)
    # https://pypi.org/project/face_recognition/
    print("[INFO] loading pickle file and face detector...")
    
    data = pickle.loads(open(args["pickle"], "rb").read())
    detector = cv2.CascadeClassifier(args["cascade"])
    print("[INFO] starting video stream...")
    
    # loop over frames from the video file stream
    while True:
        # read next frame from cam stream
        frame = vs.read()
        frame = imutils.resize(frame, width=400, height=300)
        # convert the input frame from BGR to grayscale to face detection
        # and convert BGR to RGB for face recognition
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       # define actual date and time 
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE )
        
        # OpenCV returns bounding box coordinates in (x, y, w, h) order
	    # but we need them in (top, right, bottom, left) order, so we
	    # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the face vectors from frame 
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

	    # loop over the face model
        for encoding in encodings:
            # compare the model of faces from video, and model from file
            # IMPORTANT !!! face_recognition.compare_faces
            # https://face-recognition.readthedocs.io/en/latest/face_recognition.html
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            # if face matches 
            if True in matches:
                # find the indexes of all matched faces then initialize a
			    # dictionary to count the total number of times each face
			    # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face 
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

			    # determine the recognized face with the largest number
			    # of propabilty (matches vectors)
                name = max(counts, key=counts.get)
		    
            # update the list of names
            names.append(name)
        
            # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):

            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        with lock:
            outputFrame = frame.copy()


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


@app.route("/video2")
def video():
    # return response (MIME type)
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
        # create the parser of intput arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--cascade",required=True, help="path to cascade file ")
    parser.add_argument("-p","--pickle",required=True, help="path to pickle file where encoded are face model")
    parser.add_argument("-cc","--cam", type=str, default="pc",help="option 'pc' is a webcam, 'pi' is for raspbbery pi cam")
    parser.add_argument("-i", "--ip", type=str, required=True, help="ip address of device")
    parser.add_argument("-o", "--port", type=int, required=True,help="server port number (1024 to 65535) ")
    args = vars(parser.parse_args())

    t = threading.Thread(target=detect_face)
    t.daemon = True
    t.start()
    # run flask app
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
vs.stop()