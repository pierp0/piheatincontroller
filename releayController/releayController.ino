#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define BRATE 115200
#define DEBUG false
#define IPSRV "192.168.1.100"
#define NET "test"
#define NETPASS "foo"
#define PAGEGET "getStatus"
#define PAGEPOST "postStatus"
#define PORT "12345"
#define RELAY 0     //NC relay Normally closed
#define SLEEPT 3e8

bool status = true;

void setup() {
  if (DEBUG){
     Serial.begin(BRATE);
     Serial.print("\n\t-----DEBUG----");  
  } 
  WiFi.begin(NET, NETPASS);
  if(DEBUG){
    Serial.print("\tWiFi module started...");
  }  
  while (WiFi.status() != WL_CONNECTED){
    if(DEBUG){
      Serial.print("...\n");
    }
    delay(500);
  }
  if(DEBUG){
    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
  }  
  pinMode(RELAY,OUTPUT);
  updateStatus(true);
}

void loop() {
  delay(30000);
  postStatus();
  updateStatus(getStatus());
  ESP.deepSleep(SLEEPT);
}

void updateStatus(bool s){
  if (s)
    digitalWrite(RELAY, LOW); // True close
  else
    digitalWrite(RELAY, HIGH);// False Open
  status = s;
}

void postStatus() {
  HTTPClient http;
  http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(PAGEPOST));
  http.addHeader("Content-Type", "text/plain");
  http.POST("s=" + String(status));
  http.end();
}

bool getStatus() {
  HTTPClient http;
  http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(PAGEGET));
  http.addHeader("Content-Type", "text/plain");
  http.GET();
  bool s = http.getString();
  http.end();
  return s;
}
