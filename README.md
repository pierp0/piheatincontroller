# piheatincontroller

Un po più di un semplice termostato.

Goal:
  Realizzare un dispositivo che aiuti a gestire in maniera intelligente il riscaldamento degli ambienti di casa.
  
Hardware:
  - PI : Il core del progetto è un raspberry pi 3b+ dotato di display Kuman e case. Il raspberry si occuperà di gestire sensori e relay oltre che di proporre un interfaccia web di gestione
      
![Raspberry](https://raw.githubusercontent.com/pierp0/piheatincontroller/master/IMG/770A5842-1612x1080.jpg)
    raspberry   : https://www.amazon.it/gp/product/B07BDR5PDW/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1
    microsdcard : https://www.amazon.it/gp/product/B06XFSZGCC/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1
    display     : https://www.amazon.it/gp/product/B01CNLYL1C/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1
    case        : https://www.amazon.it/gp/product/B07KYJVFB7/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1
  
  - Sensori : Il sistema prevede l'utilizzo di sensori di temperatura e umidità di tipo DHT11 (solo per test) o DHT22 i sensori sono gestiti da un controllore che comunica con il raspberry. Per fare ciò viene utilizzato un ESP8266. Il sistema è alimentato a batteria con batterie LiPo da 3.7 V 500mA
    ESP8266     : https://www.amazon.it/gp/product/B06XP74C81/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1
    programmatore per ESP : https://www.amazon.it/gp/product/B078J7LDLY/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1
    batterie    : https://www.amazon.it/dp/B01N76CXKW/ref=sr_1_12
    dht11+base  : https://www.amazon.it/gp/product/B077HYPMF6/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1
  
  - Relay : ad occuparsi dell'accezione e dello spegnimento della caldaia viene utilizzato un relay controllato sempre da un ESP8266 che comunica con il raspberry. Il relay e l'ESP8266 sono alimentati da un trasformatore AC/DC collegato alla rete elettrica.
    relay con base : https://www.amazon.it/gp/product/B07D37ZCN3/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1
    alimentatore   : https://www.amazon.it/gp/product/B07M8WLCVL/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1
    
Soft:
  Gestori hardware: 
  Server pi:
  test:
