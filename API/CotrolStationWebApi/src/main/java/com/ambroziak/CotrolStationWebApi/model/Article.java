package com.ambroziak.CotrolStationWebApi.model;

import lombok.Data;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Data
@Entity
public class Article {
    public Article(String title, String article) {
        this.title = title;
        this.article = article;
    }

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String title;

    private String article;

    @Override
    public String toString() {
        return super.toString();
    }
}
