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
import org.springframework.web.multipart.MultipartFile;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.util.HashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import java.net.URL;
import org.tensorflow.lite.Interpreter;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@RestController
public class SMSController {


      @Autowired
      private SMSService smsService;

      private final Interpreter tflite;

      public SMSController() throws IOException {
          // Load the TensorFlow Lite model
          File modelFile = new File("AI_models/mobilenetv2_finetuned_quantized.tflite");
          tflite = new Interpreter(modelFile);
      }

      @RequestMapping("/sms/send")
      public ResponseEntity<String> sendSMS() {
            ApiData apiData = new ApiData();
            apiData.setMessage("Hello");
            apiData.setUserContact("+2348100597712");
            System.out.println("accessed");
           String result =  smsService.sendSMS(apiData);
          return new ResponseEntity<>(result,HttpStatus.OK);
      }

      @PostMapping("/api/diagnose")
      public ResponseEntity<Map<String, Object>> diagnoseImage(@RequestParam("file") MultipartFile file) {
          Map<String, Object> response = new HashMap<>();
          
          try {
              // Validate file
              if (file.isEmpty()) {
                  response.put("error", "No image uploaded");
                  return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
              }
              
              // Process image
              BufferedImage image = ImageIO.read(file.getInputStream());
              float[][][][] preprocessedImage = preprocessImage(image);
              
              // Run inference
              float[][] output = new float[1][9];
              tflite.run(preprocessedImage, output);
              
              // Map results
              int predictedClass = getPredictedClass(output[0]);
              String[] classNames = {"Pepper_bell_Bacterial_spot", "Pepper_bell_healthy", "Potato_Early_blight", "Potato_Late_blight",
                     "Potato_healthy", "Tomato_Bacterial_spot", "Tomato_Early_blight",
                     "Tomato_Late_blight", "Tomato_healthy"};
              
              response.put("class", classNames[predictedClass]);
              response.put("confidence", output[0][predictedClass]);
              
              return new ResponseEntity<>(response, HttpStatus.OK);
          } catch (Exception e) {
              response.put("error", e.getMessage());
              return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
          }
      }

      @PostMapping("/sms/diagnose")
      public ResponseEntity<String> handleMMS(@RequestParam("From") String from,
                                      @RequestParam("MediaUrl0") String mediaUrl) {
          try {
              // Download image from Twilio's MediaUrl
              URL url = new URL(mediaUrl);
              BufferedImage image = ImageIO.read(url);
              
              // Preprocess image
              float[][][][] preprocessedImage = preprocessImage(image);
              
              // Run inference
              float[][] output = new float[1][9];
              tflite.run(preprocessedImage, output);
              
              // Map results
              int predictedClass = getPredictedClass(output[0]);
              String[] classNames = {"Pepper_bell_Bacterial_spot", "Pepper_bell_healthy", "Potato_Early_blight", "Potato_Late_blight",
                     "Potato_healthy", "Tomato_Bacterial_spot", "Tomato_Early_blight",
                     "Tomato_Late_blight", "Tomato_healthy"};
              
              // Format SMS response
              String diagnosisMessage = String.format(
                  "AgroScan Diagnosis: %s (Confidence: %.1f%%)\n\nRecommendation: %s",
                  classNames[predictedClass].replace("_", " "),
                  output[0][predictedClass] * 100,
                  getSimpleRecommendation(classNames[predictedClass])
              );
              
              // Send SMS response
              ApiData apiData = new ApiData();
              apiData.setUserContact(from);
              apiData.setMessage(diagnosisMessage);
              smsService.sendSMS(apiData);
              
              return ResponseEntity.ok("SMS sent successfully");
          } catch (Exception e) {
              // Send error message via SMS
              ApiData apiData = new ApiData();
              apiData.setUserContact(from);
              apiData.setMessage("Sorry, we couldn't process your image. Please ensure you sent a clear photo of the plant leaf.");
              smsService.sendSMS(apiData);
              
              return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
          }
      }

      private float[][][][] preprocessImage(BufferedImage image) {
          // Resize the image to 224x224
          BufferedImage resizedImage = new BufferedImage(224, 224, BufferedImage.TYPE_INT_RGB);
          resizedImage.getGraphics().drawImage(image, 0, 0, 224, 224, null);

          // Normalize pixel values to [0, 1] and convert to channels-first format
          float[][][][] input = new float[1][3][224][224];
          for (int y = 0; y < 224; y++) {
              for (int x = 0; x < 224; x++) {
                  int rgb = resizedImage.getRGB(x, y);
                  input[0][0][y][x] = ((rgb >> 16) & 0xFF) / 255.0f; // Red channel
                  input[0][1][y][x] = ((rgb >> 8) & 0xFF) / 255.0f;  // Green channel
                  input[0][2][y][x] = (rgb & 0xFF) / 255.0f;         // Blue channel
              }
          }
          return input;
      }

      private int getPredictedClass(float[] output) {
          int predictedClass = 0;
          float maxConfidence = output[0];
          for (int i = 1; i < output.length; i++) {
              if (output[i] > maxConfidence) {
                  maxConfidence = output[i];
                  predictedClass = i;
              }
          }
          return predictedClass;
      }

      private String getSimpleRecommendation(String condition) {
          Map<String, String> recommendations = new HashMap<>();
          recommendations.put("Pepper_bell_Bacterial_spot", "Apply copper-based fungicides and remove infected leaves.");
          recommendations.put("Pepper_bell_healthy", "Your plant appears healthy. Continue current care practices.");
          // Add more recommendations
          
          return recommendations.getOrDefault(condition, "Consult with a local agricultural expert for this condition.");
      }
}