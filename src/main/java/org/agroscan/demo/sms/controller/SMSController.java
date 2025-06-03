package org.agroscan.demo.sms.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.http.ResponseEntity;
import org.agroscan.demo.sms.model.*;
import org.agroscan.demo.sms.service.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;

@RestController
public class SMSController {


      @Autowired
      private SMSService smsService;

      @PostMapping(value = "/sms/send",produces = "application/xml")
      public ResponseEntity<String> sendSMS(@RequestParam("Body") String body,
                                            @RequestParam("From") String from,
                                            @RequestParam(name = "NumMedia", defaultValue = "0" , required = false) int numMedia,
                                            @RequestParam(name = "MediaUrl0", required = false) String mediaUrl
                                            ) throws IOException {
            ApiData apiData = new ApiData();
            System.out.println("accessed");
            apiData.setBody(body);
            apiData.setFrom(from);
            apiData.setNumMedia(numMedia);
            apiData.setMediaUrl0(mediaUrl);

          System.out.println("Body: "+body);
          System.out.println("From: "+from);
          System.out.println("NumMedia: "+numMedia);
           String result =  smsService.sendSMS(apiData);
          return new ResponseEntity<>(result,HttpStatus.OK);
      }

      @PostMapping("/smsw/send")
    public String handleWhatsappMessage(@RequestParam("Body") String body, @RequestParam("From") String from
      , @RequestParam(value = "NumMedia", required = false) int numMedia, @RequestParam(value = "MediaUrl0", required = false) String mediaUrl0
      ) {
          try {
              smsService.sendWhatsappMessage(numMedia, from, body, mediaUrl0);
          }
          catch(Exception ex) {ex.printStackTrace();}
          return "";
    }




}
