package com.ambroziak.CotrolStationWebApi.api;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import java.util.HashMap;
import java.util.Map;

@Controller
public class VideoController {
    @GetMapping("video")
    public ModelAndView video(){
        String viewName ="video.html";
        Map<String,Object> model = new HashMap<String,Object>();
        return new ModelAndView(viewName,model);
    }
}
