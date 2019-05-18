#include "Adafruit_SI1145.h"
#include "DHT.h"

// SI1145
Adafruit_SI1145 ir = Adafruit_SI1145();


// DHT22
#define DHTPIN 7
#define DHTTYPE 22
DHT dht(DHTPIN, DHTTYPE);

float hum;
float temp;

void setup() {
  Serial.begin(9600);

  // SI1145
  ir.begin();

  // DHT22
  dht.begin();
}

void loop() {
  // SI1145
  float IRvalue = ir.readIR();
  Serial.print("|");
  Serial.print(IRvalue);

  // DHT22
  hum = dht.readHumidity();
  temp = dht.readTemperature();
  Serial.print("|");
  Serial.print(hum);
  Serial.print("|");
  Serial.print(temp);
  Serial.println("|");

  delay(5000);
}

