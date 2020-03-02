RUN SENSOR MODULE:

First you must connect dht11 on raspberryPi3 port GPIO pin 7

Preper RabbitMq, you can use locally version in docker using:
#docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management

Create RabbitMq Queues named "temperature" and "humidity"
 
Copy  SensorDataSender.jar file do Raspberry

in RPI terminal call:
#java -jar SensorDataSender.jar