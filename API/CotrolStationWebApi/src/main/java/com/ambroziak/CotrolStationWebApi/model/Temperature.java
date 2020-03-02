package com.ambroziak.CotrolStationWebApi.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.time.LocalDateTime;

@Entity
public class Temperature {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Float value;
    private LocalDateTime dateTime;

    public Temperature(Float value, LocalDateTime dateTime) {
        this.value = value;
        this.dateTime = dateTime;
    }

    public Temperature() {
    }

    public Float getValue() {
        return value;
    }

    public void setValue(Float value) {
        this.value = value;
    }

    public LocalDateTime getDateTime() {
        return dateTime;
    }

    public void setDateTime(LocalDateTime dateTime) {
        this.dateTime = dateTime;
    }

    @Override
    public String toString() {
        return "Temperature{" +
                "id=" + id +
                ", value=" + value +
                ", dateTime=" + dateTime +
                '}'+"\n";
    }
}
