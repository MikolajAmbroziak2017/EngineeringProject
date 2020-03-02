# Author Mikolaj Ambroziak
# start aplication using :
# python facemodelcreator.py --input dataset --output encodings.pickle --detection cnn
# or if use on raspberry pi 3 :
# python facemodelcreator.py --input dataset --output encodings.pickle --detection log
# This code crate a pickle file. Encoded faces from image file at dataset

# all necessary imports 
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# parser of input options in console
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",required=True,help="path to input directory dataset of face images")
    parser.add_argument("-o","--output",required=True,help="path to output serialized db of encoded faces ***.pickle")
    parser.add_argument("-d", "--detection", type=str, default="cnn" ,help="face detection model to use: either `hog` or `cnn`")
    args = vars(parser.parse_args())


# taking listo of image file 
print("[INFO] Read inputs...")
imagePaths=list(paths.list_images(args["input"]))
print("1")
tableEncodings = []
names = []

for (i, imagePath) in enumerate(imagePaths):
    print("[INFO] Processing image...{}/{}".format(i + 1,len(imagePaths)))
    name = imagePath.split(os.path.sep)[-2]

    # reading images file 
    image = cv2.imread(imagePath)
    # convert color BRG(openCV default color) to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # https://pypi.org/project/face_recognition/
    # recognition face using face_recognition class for python 
    # faceCoordinate is a table with coordinates of the human face
    faceCoordinate = face_recognition.face_locations(rgb, model=args["detection"])
    print("2")
    # encode face embedding (osadzenie twarzy) in model
    encodings = face_recognition.face_encodings(rgb,faceCoordinate)

    #saving model in table
    for encoding in encodings:
        print("5")
        tableEncodings.append(encoding)
        names.append(name)

# Create and save pickle file
print("[INFO] Creating Pickle File...")
data = {"encodings": tableEncodings, "names": names}
f = open (args["output"],"wb")
f.write(pickle.dumps(data))
f.close 
print("[INFO] Process create model succesfull")