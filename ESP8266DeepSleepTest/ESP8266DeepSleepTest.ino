/**************************************************************************************************/
/**                              ESP8266 deep sleep test                                         **/
/**           Version 0.9 - https://github.com/pierp0/piheatincontroller                         **/
/**                      Written By Pierpaolo Furiani (2019)                                     **/
/**************************************************************************************************/


void setup() {
  Serial.begin(115200);
  delay(3000);
  Serial.println("\n-------------ESP8266 DEEP SLEEP TEST-------------");
}

void loop() {
  delay(2000);
  Serial.println("I'm awake!");
  Serial.println("Preparing for deep sleep...");
  ESP.deepSleep(1000);
}
