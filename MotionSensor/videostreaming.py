from camdetector.detector import MotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
# inicjacja ramki wyjściowej blokada obiektu dla bezpieczenstwa
outputFrame = None
lock = threading.Lock()

# inicjalizacja obiektu flask
app =Flask(__name__)

# inicjalizacja video stream oraz zezwolenie na uruchomienie kamery
# Dla PiCamera: 
vs = VideoStream(usePiCamera=1).start()

# Dla USB Cam:
# vs = VideoStream(src=0).start()
time.sleep(2.0) 

@app.route("/")
def index():
    # zwraca wyrenderowane template
    return render_template("index.html")

# frameCount to minimalna ilość klatek do zbudowania tła
def detect_motion(frameCount):
    global vs, outputFrame, lock

    # inicjalizacja detektora 
    md = MotionDetector(accumWeight=0.1)
    total = 0

    # pętla na klatkach z video stream
    while True:
        # wczytywanie kolejnej klatki ze stream'u, 
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # przekształcenie obrazu klatki z BGR w odcieniu szarości
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        # użycie filtru Gaussa redukcja szumu  DO OPISANIA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # zdefiniowanie czasu i narysowanie na ramce
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        # jeżeli osiągnięto wystarczającą ilość klatek do zbudowania 
        # tła przechodzimy do konntynuacji przetwarzania ramki obrazu
        if total > frameCount:
            # detekcja ruchu na obrazie
            motion = md.detect(gray)
            
            # sprawdzenie ruchu na obrazie z kamerki
            if motion is not None:
                # wczytanie wartości max i min ruchu                  
                # narysowanie obwiedni wokoło ruchu
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),(0, 0, 255), 2)
        
        # update modelu tła i inkrementacja totalnej liczby 
        # klatek wczytanych do tej pory
        md.update(gray)
        total += 1

        # wykorzystując lock wymaganą do obsługi współbieżności wątków 
        # przypisujemy ramce wyjsciowej ramkę którą uzyskaliśmy podczas przetwarzania
        # musimy uzyskać blokadę aby klient nie odczytał jej podczas próby aktualizacji 
        with lock:  
            outputFrame = frame.copy()

def generate():
    # pobranie globalnych referencji 
    global outputFrame, lock

    # pętla na ramkach strumienia wyjściowego
    while True:
        # zatrzymanie akcji do czasu 'otrzymania' locka 
        with lock:
            if outputFrame is None:
                continue
            # kodowanie ramki w formacie JPEG 
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # warunek poprawnosci kodowania
            if not flag:
                continue

        # zwrócenie ramki wyjściowej w formacie bajtowym
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video")
def video():
    # zwraca wygenerowaną odpowiedź (MIME type)
    return Response(generate(), mimetype= "multipart/x-mixed-replace; boundary=frame")

# main 
if __name__ == '__main__':
    # konstruowanie parsera argumentów wiersza poleceń
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of device")
    ap.add_argument("-o", "--port", type=int, required=True,help="server port number (1024 to 65535) ")
    ap.add_argument("-f", "--frame-count", type=int, default=32, help="number of frame to construct background model")
    args=vars(ap.parse_args())

    # uruchomienie wątku wykrywania ruchu
    t  = threading.Thread(target=detect_motion, args=(args["frame_count"],))
    t.daemon = True
    t.start()

    # uruchomienie flask app 
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)
vs.stop()
