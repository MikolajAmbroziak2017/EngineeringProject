package pl.ambroziak.sensorapp.Model;

import java.io.Serializable;
import java.time.LocalDateTime;


public class SeriesData implements Serializable {

    private static final long serialVersionUID = 8328986821565744634L;

    /**
     * Date representing a time of obtaining a value.
     *
     */
    private LocalDateTime gainDate;

    /**
     * Value such as an average of temperature measurements or humidity.
     */
    private String value;

    public SeriesData(LocalDateTime gainDate, String value) {
        this.gainDate = gainDate;
        this.value = value;
    }

    public SeriesData() {
    }

    public static long getSerialVersionUID() {
        return serialVersionUID;
    }

    public LocalDateTime getGainDate() {
        return gainDate;
    }

    public void setGainDate(LocalDateTime gainDate) {
        this.gainDate = gainDate;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
