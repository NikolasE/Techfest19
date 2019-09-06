#include <Arduino.h>
#include <Tle5012b.h>

Tle5012b Tle5012MagneticAngleSensor = Tle5012b();

const char SEP = ':';

void setup() {
  while(!Serial)
    ;
  Serial.begin(115200);
  Tle5012MagneticAngleSensor.begin();
}

void loop() {
  double d = 0.0;
  int16_t b = 0;

  Tle5012MagneticAngleSensor.getAngleSpeed(d);
  Serial.print(d);
  Serial.print(SEP);

  Tle5012MagneticAngleSensor.getAngleValue(d);
  Serial.print(d);
  Serial.print(SEP);

  Tle5012MagneticAngleSensor.getNumRevolutions(b);
  Serial.print(b);
  Serial.print('\n');

  delay(10);
}