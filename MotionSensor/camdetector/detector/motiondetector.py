import numpy as np
import imutils
import cv2

class MotionDetector:
    def __init__(self, accumWeight=0.5):
        self.accumWeight =accumWeight

        # inicjalizacja modelu tła 
        self.bg = None

    def update(self, image):
        # jeżeli model tła jest None, metoda inicjalizuje go
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return

        # wyliczenie modelu tła z image   
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)
    
    def detect(self, image, tVal=25):
        # obliczenie różnicy między modelem tła a przekazanym obrazem  
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        
        # usuwanie szumu, to znaczy odfiltrowywania pikseli o 
        # zbyt małych lub zbyt dużych wartości. 
        # https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html?highlight=threshold#cv2.threshold
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]

        # wykonuje serie wygładzań i rozprężeń obrazu w celu 
        # usunięcia małych plam 
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # znajdywanie konturów na obrazie progowym i zainicjowanie
        # ich maksymalnych boxów regionu ruchu
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # max rozmiary ramki to nieskończoność 
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # zwraca None jeżeli nie ma znalezionych konturów 
        if len(cnts) == 0:
            return None

        for c in cnts:
            # Dla każdego konturu obliczamy obwiednię, a następnie aktualizujemy
            # nasze zmienne, znajdując współrzędne minimum i maksimum (x, y), które zmieniły się podczas ruchu
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))
        
        return (thresh, (minX, minY, maxX, maxY))