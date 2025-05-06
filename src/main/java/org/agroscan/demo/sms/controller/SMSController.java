package org.agroscan.demo.sms.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.http.ResponseEntity;
import org.agroscan.demo.sms.model.*;
import org.agroscan.demo.sms.service.*;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.HttpStatus;

@RestController
public class SMSController {


      @Autowired
      private SMSService smsService;

      @RequestMapping("/sms/send")
      public ResponseEntity<String> sendSMS() {
            ApiData apiData = new ApiData();
            apiData.setMessage("Hello");
            apiData.setUserContact("+2348100597712");
            System.out.println("accessed");
           String result =  smsService.sendSMS(apiData);
          return new ResponseEntity<>(result,HttpStatus.OK);
      }

}