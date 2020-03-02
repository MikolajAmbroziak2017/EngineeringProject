package com.ambroziak.CotrolStationWebApi.repository;

import com.ambroziak.CotrolStationWebApi.model.Humidity;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface HumidityRepo extends CrudRepository<Humidity,Long> {
}
