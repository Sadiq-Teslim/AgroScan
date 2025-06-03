package org.agroscan.demo.sms.service;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.twilio.twiml.MessagingResponse;
import com.twilio.twiml.messaging.Body;
import com.twilio.twiml.messaging.Media;
import com.twilio.twiml.messaging.Message;
import org.agroscan.demo.sms.response.DataResponse;
import org.agroscan.demo.sms.response.Response;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.twilio.type.PhoneNumber;
import com.twilio.Twilio;
import org.agroscan.demo.sms.model.*;

import java.awt.image.BufferedImage;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLConnection;
import java.util.*;

import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import javax.imageio.ImageIO;

@Service
public class SMSService {


      @Value("${agroscan-account-sid}")
      private String ACCOUNT_SID;  
      @Value("${agroscan-auth-token}")
      private String AUTH_TOKEN;
      @Value("${agroscan-dev-num}")
      private String DEV_NUM;
      @Value("${diagnosis-key}")
      private String dkey;

      @Autowired
      private RestTemplate restTemplate;
      private ObjectMapper objectMapper;
      private String path = System.getProperty("java.io.tmpdir");
      private Logger logger = LoggerFactory.getLogger(SMSService.class);
      public String sendSMS(ApiData apiData) {
             Response response = null;
             objectMapper = new ObjectMapper();
             try {
                 if(apiData.getNumMedia() > 0) {
                     if(!Objects.isNull(apiData.getMediaUrl0())) {
                         apiData.setImage(getFilefromUrl(apiData.getMediaUrl0()));
                         response = readApi(apiData);
                     }
                 }
                 else {
                     response = readApi(apiData);
                 }
             }
             catch(Exception e) {
                 System.out.println("ERROR: "+e.getMessage());
                 logger.error("ERROR: {}",e.getMessage());
             }

             Twilio.init(ACCOUNT_SID, AUTH_TOKEN);

          System.out.println(response);
            String value = "";
            logger.info("authenticated and authorised");
            if(!Objects.isNull(apiData)) {
                 if(!Objects.isNull(response)) {

                     String format = extractData(response);
                     Body responseBody = new Body.Builder(format).build();
                     Media media = new Media.Builder(apiData.getMediaUrl0()).build();
                     Message message = null;
                     if(!Objects.isNull(apiData.getMediaUrl0())) {
                         message = new Message.Builder()
                                 .body(responseBody)
                                 .media(media)
                                 .build();
                     }
                     else {
                         message = new Message.Builder()
                                 .body(responseBody)
                                 .build();
                     }

                     MessagingResponse twiml = new MessagingResponse.Builder()
                             .message(message)
                             .build();

                     value=twiml.toXml();
                     logger.info("message has been sent successfully with response : {}", twiml.toXml());

                 }
            }
         return value;
    }

    public String extractData(Response response) {
        DataResponse dataResponse = Objects.requireNonNull(response.getData());

        String format = "\nDiagnosis Title: "+dataResponse.getDiagnosis_title()+
                "\nHealth Condition: "+dataResponse.getHealth_condition()+
                "\nCause: "+dataResponse.getCause()+
                "\nControl: "+dataResponse.getControl_suggestions()+
                "\nDisease Signs: "+dataResponse.getDisease_signs()+
                "\nSummary: "+dataResponse.getSummary();

        return format;
    }

    public void sendWhatsappMessage(int numMedia,String ...data) throws IOException, URISyntaxException {
          Twilio.init(ACCOUNT_SID,AUTH_TOKEN);

          ApiData apiData = new ApiData();
          apiData.setBody(data[1]);
          apiData.setImage(new File(path,"test.jpg"));
          apiData.setFrom(data[0]);

        System.out.println(data[2]);
        File outputFile = getFilefromUrl(data[2]);
        System.out.println(outputFile.exists());
        apiData.setImage(outputFile);
          com.twilio.rest.api.v2010.account.Message message = com.twilio.rest.api.v2010.account.Message.creator(
                  new PhoneNumber(data[0]),
                  new PhoneNumber("whatsapp:+14155238886"),
                  extractData(readApi(apiData))
          ).create();
        System.out.println(message.getAccountSid());
    }

    public File getFilefromUrl(String url) {
            String msg = "";
          try {
              URL objUrl = new URL(url);
              HttpURLConnection connection = (HttpURLConnection) objUrl.openConnection();

              String credentials = ACCOUNT_SID+":"+AUTH_TOKEN;
              String basicAuth = "Basic "+Base64.getEncoder().encodeToString(credentials.getBytes());

              connection.setRequestProperty("Authorization",basicAuth);
              InputStream is = connection.getInputStream();
              BufferedImage bufferedImage = ImageIO.read(is);

              if(bufferedImage != null) {
                  File outputFile = new File(path,"test.jpg");
                  ImageIO.write(bufferedImage,"jpg",outputFile);
                  return outputFile;
              }
          }
          catch(Exception e) {
              System.out.println(e.getMessage());
          }
          return null;
    }

    private Response readApi(ApiData apiData) throws IOException, URISyntaxException {
          String url = "https://agroscan-xasy.onrender.com/new-chat/sms-diagnosis";

        File file = apiData.getImage();
        FileSystemResource fileResource = new FileSystemResource(file);

        MultiValueMap<String,Object> body = new LinkedMultiValueMap<>();
        body.add("text",apiData.getBody());
        body.add("image",fileResource);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        headers.set("Diagnosis-Key",dkey);

        HttpEntity<MultiValueMap<String,Object>> requestEntity =
                new HttpEntity<>(body,headers);
        ResponseEntity<Response> response = restTemplate
                .postForEntity(url,requestEntity,Response.class);
        System.out.println(response.getBody().toString());
        return response.getBody();

    }

}