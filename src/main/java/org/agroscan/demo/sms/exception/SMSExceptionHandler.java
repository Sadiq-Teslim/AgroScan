package org.agroscan.demo.sms.exception;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import com.twilio.exception.TwilioException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@RestControllerAdvice
public class SMSExceptionHandler {

     private Logger logger = LoggerFactory.getLogger(SMSExceptionHandler.class);
     @ExceptionHandler(TwilioException.class)
     public void handleSmsException(TwilioException twilioException) {
         System.out.println(twilioException.getMessage());
          logger.error("An error occurred!! : {}" , twilioException.getMessage());
    }
}