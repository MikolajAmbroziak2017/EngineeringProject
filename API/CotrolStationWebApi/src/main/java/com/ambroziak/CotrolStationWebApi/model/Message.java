package com.ambroziak.CotrolStationWebApi.model;

import lombok.Data;
import org.springframework.web.bind.annotation.ModelAttribute;
@Data
public class Message {
    private String mess;

    public String getMessage() {
        return mess;
    }

    public void setMessage(String message) {
        this.mess = message;
    }

    @Override
    public String toString() {
        return "Message{" +
                "message='" + mess + '\'' +
                '}';
    }
}
