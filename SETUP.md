# AgroScan Setup Instructions

## Prerequisites
- Java JDK 11+
- Maven
- Twilio account (for SMS functionality)

## Backend Setup
1. Clone the repository
2. Navigate to the project directory
3. Run `mvn install`
4. Configure application.properties with your Twilio credentials
5. Run `mvn spring-boot:run`

## Frontend Setup
No build step needed - open index.html in a browser.

## SMS Configuration
1. Set up a Twilio account
2. Configure a phone number with MMS capabilities
3. Set the webhook URL to your `/sms/diagnose` endpoint