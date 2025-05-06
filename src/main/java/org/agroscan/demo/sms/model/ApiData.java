package org.agroscan.demo.sms.model;

public class ApiData {

     private Long id;
     private String message;
     private String userContact;

      public Long getId() {
    return id;
}

public void setId(Long id) {
    this.id = id;
}

public String getMessage() {
    return message;
}

public void setMessage(String message) {
    this.message = message;
}

public String getUserContact() {
    return userContact;
}

public void setUserContact(String userContact) {
    this.userContact = userContact;
}
}
