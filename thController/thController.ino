/**************************************************************************************************/
/**Client ESP8266 on DHT11/DHT22 boar. Post temperature and humidity to PiHeatinController Server**/
/**           Version 0.9 - https://github.com/pierp0/piheatincontroller                         **/
/**                      Written By Pierpaolo Furiani (2019)                                     **/
/**************************************************************************************************/

#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

//Warning: use DHT11 only for test (accuracy of 2 celsius degrees). DHT22 in production (accuracy of 0,5 celsius degrees)
#define DHTPIN 2
#define DHTTYPE DHT11 // Or DHT22
#define SLEEPT 3e8    // Time in ms used for deep sleep. 5 minuts it's default

const bool  DEBUG = true;        // If it's true it will print on serial port
const char* IPSRV = "127.0.0.1";  // Replace with the ip address of the server.
const char* PORT  = "12345";      // Replace with server port
const char* SSID  = "EGGS";       // Replace with yor network SSID
const char* PWD   = "SPAM";       // Replace with your net pasword
const char* POSTPAGE   = "postHT";    // Is the server page used for POST, don't touch it.
const char* HELLOPAGE  = "postHello"; // Page used to signal that the sensor is activated

float tmp, hty;

DHT dht(DHTPIN, DHTTYPE);


void setup() {
  if (DEBUG){
    delay(5000);
    Serial.begin(115200);
    Serial.println("\n-----DEBUG-----");  
  }
  
  // DHT initialization
  dht.begin();
  if(DEBUG) 
    Serial.println("DHT module started...");

  // WiFi initialization
  WiFi.begin(SSID, PWD);
  if(DEBUG) 
    Serial.println("WiFi module started...");
  
  // Trying to connect...
  while (WiFi.status() != WL_CONNECTED){
    if(DEBUG) 
      Serial.println("...\n");
    delay(3000);
  }
  
  // Connectd!
  if(DEBUG)
    Serial.println("Connected, IP address: " + WiFi.localIP());
    
  // Send an hello message to the server (MAC address) 
  int srvResponse = sayHello();
  if(DEBUG)
    Serial.println('Sensor say hello to the server\nServer say back: ' + String(srvResponse));
}


void loop() {
  HTTPClient http;
  
  // Read temperature & humidity from senson
  dht.read(DHTPIN);
  tmp = dht.readTemperature();
  hty = dht.readHumidity();

  // Error check
  if (isnan(hty) || isnan(tmp)) {
    if (DEBUG) 
      Serial.println("Failed to read from DHT sensor!");
    else{
      http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(POSTPAGE));
      http.addHeader("Content-Type", "text/plain");
      http.POST("ERR=" + WiFi.macAddress());
    }  
  }else{
    if (DEBUG){
      Serial.println("\nTemperature\t:\t" + String(tmp));
      Serial.println("\nHumidity\t:\t" + String(hty));    
    }
    http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(POSTPAGE));
    http.addHeader("Content-Type", "text/plain");
    http.POST("r=" + WiFi.macAddress() + "&t=" + String(tmp) + "&h=" + String(hty));
  }
  http.end();
  
  // Deep sleep for SLEEPT time. For deep sleep function hardware modify is needed, please refer to documentation.
  ESP.deepSleep(SLEEPT);
}


int sayHello(){
  HTTPClient http;
  http.begin("http://" + String(IPSRV) + ":" + String(PORT) + "/" + String(HELLOPAGE));
  http.addHeader("Content-Type", "text/plain");
  
  // The sensor send it's MAC address. If everything goes right the server say back 200
  int httpRetCode = http.POST("hello=" + WiFi.macAddress());
  http.end();
  return httpRetCode;
}
