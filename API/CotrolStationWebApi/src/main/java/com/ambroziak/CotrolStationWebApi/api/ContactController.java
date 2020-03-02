package com.ambroziak.CotrolStationWebApi.api;

import com.ambroziak.CotrolStationWebApi.model.Message;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.HttpRequestHandler;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.net.http.HttpResponse;
import java.util.HashMap;
import java.util.Map;

@Controller
public class ContactController {
    @Autowired
    Api api;
    @RequestMapping(value = "/contact", method = RequestMethod.GET)
    public ModelAndView contact(){
        String viewName ="contact.html";
        Map<String,Object> model = new HashMap<String,Object>();
        model.put("test","test wartosci kurde bele");
        return new ModelAndView(viewName,model);
    }
    @PostMapping("/hasSent")
    public ModelAndView postMessage(@RequestBody String o){
              String viewName ="hasSent.html";
        Map<String,Object> model = new HashMap<String,Object>();
        model.put("obiekt",o);
        return new ModelAndView(viewName,model);
    }
    @GetMapping("/hasSent")
    public ModelAndView getMessage(){
        String viewName ="hasSent.html";
        Map<String,Object> model = new HashMap<String,Object>();
       return new ModelAndView(viewName,model);
    }
}
