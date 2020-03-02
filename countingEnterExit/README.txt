RUN Object Counter

This program will counting people who enter or leave space

check video cam port:
for RPI cam
# vs = VideoStream(usePiCamera=1).start() 

for USB cam
# vs = VideoStream(src=0).start()

Use peopleCounterFile calling:
#python peopleCounter.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model 
mobilenet_ssd/MobileNetSSD_deploy.caffemodel --ip 0.0.0.0 --port 8000
