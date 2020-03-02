Monitoring Area Station

Author Mikolaj Ambroziak

########################################################################################################

RUN SENSOR MODULE:

First you must connect dht11 on raspberryPi3 port GPIO pin 7

Preper RabbitMq, you can use locally version in docker using:
#docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

Create RabbitMq Queues named "temperature" and "humidity"
 
Copy  SensorDataSender.jar file do Raspberry

in RPI terminal call:
#java -jar SensorDataSender.jar

########################################################################################################

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

########################################################################################################

RUN MOTION SENSOR

check video cam port:
for RPI cam
# vs = VideoStream(usePiCamera=1).start() 

for USB cam
# vs = VideoStream(src=0).start()

You can use videostreaming file calling 
python3 videostreaming.py --ip 0.0.0.0 --port 8000 

"--ip" it a address ip of your machine
"--port" server port

########################################################################################################

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

########################################################################################################

RUN CONTROL STATION WEBAPI

using docker you can create localy RabbitMq and mysql database

MySql:
#docker run --name name -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=nameOfDB -d -p 3306:3306 -d mysql

RabbitMq:
#docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
in rabbit is required to create 2 queues named "humidity" and "temperature"

To RUN application you must change a application.properties:

spring.jpa.hibernate.ddl-auto=update
spring.datasource.url=jdbc:mysql://DataBaseIP/SE
spring.datasource.username=username
spring.datasource.password=password
spring.thymeleaf.cache=false
spring.rabbitmq.host=RabbitMqIP
spring.rabbitmq.virtual-host=/
spring.rabbitmq.password=password
spring.rabbitmq.username=username

Change templates-> video.html 
object <p id="videobuttons"> 

find <button class="onclick" onclick="document.getElementById('video').src='http://IP CAM ADDRESS/video'">
and set ip cam module ip address

default loging in application with :

username : user
password : user

for admin 

username : admin
password : admin


