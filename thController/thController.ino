#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define BRATE 115200
#define DEBUG false
#define DHTPIN 2
#define DHTTYPE DHT11
#define IPSRV "192.168.1.100"
#define NET "RIGEL2.4"
#define NETPASS "PIPPOpsg1mp5"
#define PAGE "postHT"
#define PORT "12345"
#define ROOM 2
#define SLEEPT 3e8

DHT dht(DHTPIN, DHTTYPE);

float tmp = 0.00;
float hty = 0.00;

void setup() {
  if (DEBUG){
    Serial.begin(BRATE);
    Serial.print("\n\t-----DEBUG----");  
  }
  dht.begin();
  if(DEBUG){
    Serial.print("\tDHT module started...");
  }  
  WiFi.begin(NET, NETPASS);
  if(DEBUG){
    Serial.print("\tWiFi module started...");
  }  
  while (WiFi.status() != WL_CONNECTED){
    if(DEBUG){
      Serial.print("...\n");
    }
    delay(3000);
  }
  if(DEBUG){
    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
  }  
}

void loop() {
  delay(10000);
  HTTPClient http;
  /*http.begin("http://192.168.1.100:12345/postHT");*/
  /*http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(PAGE));*/
  dht.read(DHTPIN);
  tmp = dht.readTemperature();
  hty = dht.readHumidity();
  if (isnan(hty) || isnan(tmp)) {
    if (DEBUG) {
      Serial.println("Failed to read from DHT sensor!");
    }
    else{
       http.begin("http://192.168.1.100:12345");
       http.addHeader("Content-Type", "text/plain");
       /*http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(PAGE));*/
      http.POST("ERR=Errorroom" + String(ROOM));
    }  
    return;
  }else{
    if (DEBUG){
      Serial.print("\nTemperature\t:\t");
      Serial.print(tmp);
      Serial.print("\nHumidity\t:\t");
      Serial.print(hty);     
    }
    else{
      /*http.begin("http://192.168.1.100:12345/postHT");*/
      http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(PAGE));
      http.addHeader("Content-Type", "text/plain");
      http.POST("r=" + String(ROOM) + "&t=" + String(tmp) + "&h=" + String(hty));
    }
  }
  http.end();
  /*ESP.deepSleep(SLEEPT);*/
}
