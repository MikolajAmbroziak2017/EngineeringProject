YOU MUST INSTALL ADDITIVES
# pip install flask
# pip install numpy
# pip install opencv-contrib-python
# pip install imutills

RUN APLICATION :
$ python3 videostreaming.py --ip 0.0.0.0 --port 8000 
"--ip" it a address ip of your machine
"--port" server port

you can also add "--frame-count" option

"--frame-count" how many frames you use to create background model (default 32)

#!/usr/bin/env python
# -*- coding: utf-8 -*- 