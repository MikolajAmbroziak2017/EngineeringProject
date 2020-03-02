package com.ambroziak.CotrolStationWebApi.repository;

import com.ambroziak.CotrolStationWebApi.model.Temperature;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TemperatureRepo extends CrudRepository<Temperature,Long> {
}
