/**************************************************************************************************/
/**Client ESP8266 to manage relay controller. Post actual status and get next status             **/
/**           Version 0.9 - https://github.com/pierp0/piheatincontroller                         **/
/**                      Written By Pierpaolo Furiani (2019)                                     **/
/**************************************************************************************************/

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define RELAY 0     // NC relay Normally closed
#define SLEEPT 3e8  // Time in ms used for deep sleep. 5 minuts it's default

const bool  DEBUG = true;         // If it's true it will print on serial port
const char* IPSRV = "127.0.0.1";  // Replace with the ip address of the server.
const char* PORT  = "12345";      // Replace with server port
const char* SSID  = "EGGS";       // Replace with yor network SSID
const char* PWD   = "SPAM";       // Replace with your net pasword
const char* GETPAGE   = "getNextStatus"; // Used to get the next relay status
const char* POSTPAGE  = "postStatus";    // Used to post actual relay status

bool status = true;

void setup() {
  if (DEBUG){
    delay(5000);
    Serial.begin(115200);
    Serial.print("\n\t-----DEBUG----");  
  }

  // WiFi initialization
  WiFi.begin(SSID, PWD);
  if(DEBUG)
    Serial.print("\tWiFi module started...");
  
  // Trying to connect...
  while (WiFi.status() != WL_CONNECTED){
    if(DEBUG)
      Serial.print("...\n");
    delay(3000);
  }
  
  // Connectd!
  if(DEBUG)
    Serial.println("Connected, IP address: " + WiFi.localIP());
  
  // Set pin RELAY for output
  pinMode(RELAY,OUTPUT);
  if(DEBUG)
    Serial.println("Output pin is ready");
  
  // Set actual operation status 
  updateStatus(status);
  if(DEBUG)
    Serial.println("Status updated");
}

void loop() {
  // Send a message to server with actual status
  postStatus();
  if(DEBUG)
    Serial.println();
  // Get from server the new nex status
  updateStatus(getStatus());

  // Deep sleep for SLEEPT time. For deep sleep function hardware modify is needed, please refer to documentation.
  ESP.deepSleep(SLEEPT);
}

void updateStatus(bool s){
  // Warning: relay is Normally Closed
  if (s)
    digitalWrite(RELAY, LOW); // True --> Close
  else
    digitalWrite(RELAY, HIGH);// False --> Open
  status = s;
  return;
}

void postStatus() {
  HTTPClient http;
  http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(POSTPAGE));
  http.addHeader("Content-Type", "text/plain");
  http.POST("s=" + String(status));
  http.end();
  return;
}

bool getStatus() {
  HTTPClient http;
  http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(GETPAGE));
  http.addHeader("Content-Type", "text/plain");
  http.GET();
  bool s = http.getString();
  http.end();
  return s;
}
