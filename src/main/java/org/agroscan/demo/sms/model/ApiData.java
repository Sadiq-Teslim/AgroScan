package org.agroscan.demo.sms.model;

import java.io.File;

public class ApiData {

     private String body;
     private File image;
     private int NumMedia;
     private String mediaUrl0;
     private String from;

    public String getBody() {
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public File getImage() {
        return image;
    }

    public void setImage(File image) {
        this.image = image;
    }

    public int getNumMedia() {
        return NumMedia;
    }

    public void setNumMedia(int numMedia) {
        NumMedia = numMedia;
    }

    public String getMediaUrl0() {
        return mediaUrl0;
    }

    public void setMediaUrl0(String mediaUrl0) {
        this.mediaUrl0 = mediaUrl0;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }
}
