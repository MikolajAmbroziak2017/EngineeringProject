RUN FACE RECOGNITION 

facerecognition.py is a application that recognizes faces from input model (pickle file)
in real time cam, and stream video live to the website 
 
check video cam port:
for RPI cam
# vs = VideoStream(usePiCamera=1).start() 

for USB cam
# vs = VideoStream(src=0).start()

Use this file in that way:
#python facerecognition.py --cascade cascade.xml --pickle encodings.pickle --ip 0.0.0.0 --port 8000
as function parameters set ip addres and aplications ports
 

RUN FACE MODEL CREATOR

start aplication using :
python facemodelcreator.py --input dataset --output encodings.pickle --detection cnn

or if use on raspberry pi 3 :
python facemodelcreator.py --input dataset --output encodings.pickle --detection log
This code crate a pickle file. Encoded faces from image file at dataset
