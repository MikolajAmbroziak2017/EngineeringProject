package com.ambroziak.CotrolStationWebApi.api;

import com.ambroziak.CotrolStationWebApi.model.Article;
import com.ambroziak.CotrolStationWebApi.model.Humidity;
import com.ambroziak.CotrolStationWebApi.model.SeriesData;
import com.ambroziak.CotrolStationWebApi.model.Temperature;
import com.ambroziak.CotrolStationWebApi.repository.HumidityRepo;
import com.ambroziak.CotrolStationWebApi.repository.TemperatureRepo;
import javafx.scene.chart.XYChart;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

@Controller
public class Api {
    private ArrayList<Article> list;
    private TemperatureRepo temperatureRepo;
    private HumidityRepo humidityRepo;
    private RabbitTemplate rabbitTemplate;
    private Temperature lastChangeT;
    private Humidity lastChangeH;
    @Autowired
    public Api(RabbitTemplate rabbitTemplate,HumidityRepo humidityRepo,TemperatureRepo temperatureRepo){
        this.temperatureRepo=temperatureRepo;
        this.humidityRepo=humidityRepo;
        this.rabbitTemplate=rabbitTemplate;
        lastChangeT=new Temperature(0.0F, LocalDateTime.now());
        lastChangeH=new Humidity(0.0F, LocalDateTime.now());
        list=new ArrayList<Article>();
        list.add(new Article("Warstwa Sprzętowa","<p>System kontroli otoczenia opiera sie module video. Moduł ten powstał przy wykorzystaniu RaspberryPi 3...</p>"));
        list.add(new Article("Rozpoznawanie ruchu","<p>Podsystem rozpoznawania ruchu pozwala na monitorowanie otoczenia w czasie rzeczywistym...  </p>"));
        list.add(new Article("Technologie","<p>Zapewne ciekawi Cię jakie technologie i techniki zostały użyte do stworzenia tego systemu. Zacznijmy może od...</p>"));
    }
    @GetMapping("/")
    public String firstPage(){
        return "<a href='http://localhost:8080/api'>Logowanie</a>";
    }
    @GetMapping("/index.html")
    public ModelAndView index(){
        String viewName ="index.html";
        Map<String,Object> model = new HashMap<String,Object>();
        model.put("test","test wartosci kurde bele");
        return new ModelAndView(viewName,model);
    }
    @GetMapping("/article")
    public ModelAndView getarticle(@RequestParam("id") Long number) {
        String viewName ="article.html";
        Map<String,Object> model = new HashMap<String,Object>();
        if(number==1)
            model.put("article",list.get(0).toString());
        else if(number==2)
            model.put("article",list.get(1).toString());
        else if(number==3)
            model.put("article",list.get(2).toString());
        else model.put("article", "");

        return new ModelAndView(viewName,model);
    }


    public void showData() {
      try {
          pl.ambroziak.sensorapp.Model.SeriesData humidity = (pl.ambroziak.sensorapp.Model.SeriesData) rabbitTemplate.receiveAndConvert("humidity");
          pl.ambroziak.sensorapp.Model.SeriesData temperature = (pl.ambroziak.sensorapp.Model.SeriesData) rabbitTemplate.receiveAndConvert("temperature");

      System.out.println(humidity.toString()+" "+temperature.toString());
        if(humidity!=null){
            Humidity h1=new Humidity(Float.parseFloat(humidity.getValue()),humidity.getGainDate());
            lastChangeH=h1;
            humidityRepo.save(h1);
        }
        if(temperature!=null){
            Temperature t1=new Temperature(Float.parseFloat(temperature.getValue()),temperature.getGainDate());
            lastChangeT=t1;
            temperatureRepo.save(t1);
        }}catch (Exception e){System.out.println("nie było wiadomości");}
    }

    @GetMapping("/weather")
    public ModelAndView weather() {
        showData();
        String viewName = "weather.html";
        Map<String, Object> model = new HashMap<String, Object>();
        model.put("humidity", lastChangeH.getValue().toString());
        model.put("lastH", lastChangeH.getDateTime().toString());
        model.put("temperature", lastChangeT.getValue().toString());
        model.put("lastT", lastChangeT.getDateTime().toString());
        return new ModelAndView(viewName, model);
    }
    @GetMapping("/db")
    public ModelAndView db(){
        String viewName= "db.html";
        String temperature= temperatureRepo.findAll().toString();
        String humidity=humidityRepo.findAll().toString();
        Map<String,Object> model= new HashMap<>();
        model.put("db",temperature+"\n"+humidity);
        return new ModelAndView(viewName,model);

    }

    @PostMapping("/config")
    public String setConfiguration(){
        return "setconfig";
    }
    @GetMapping("/index-onepage.html")
    public ModelAndView indexonepage(){
        String viewName ="index-onepage.html";
        return new ModelAndView(viewName);
}
