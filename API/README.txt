
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
