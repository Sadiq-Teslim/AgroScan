package org.agroscan.demo.sms.service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.twilio.type.PhoneNumber;
import com.twilio.Twilio;
import org.agroscan.demo.sms.model.*;
import java.util.*;
import com.twilio.rest.api.v2010.account.Message;
@Service
public class SMSService {


      @Value("${agroscan-account-sid}")
      private String ACCOUNT_SID;  
      @Value("${agroscan-auth-token}")
      private String AUTH_TOKEN;
      @Value("${agroscan-dev-num}")
      private String DEV_NUM;

      private Logger logger = LoggerFactory.getLogger(SMSService.class);
      public String sendSMS(ApiData apiData) {
             Twilio.init(ACCOUNT_SID, AUTH_TOKEN);
             String response = "";
            logger.info("authenticated and authorised");
            if(!Objects.isNull(apiData)) {
             Message message = Message.creator(
                 new PhoneNumber(apiData.getUserContact()),
                 new PhoneNumber(DEV_NUM),
                 apiData.getMessage()
             ).create();
            response= "message has been sent successfully with id : "+message.getSid()+" and status: "+message.getStatus();
            logger.info("message has been sent successfully with id : {} and status: {}", message.getSid(), message.getStatus());
          }
         return response;
    }

}