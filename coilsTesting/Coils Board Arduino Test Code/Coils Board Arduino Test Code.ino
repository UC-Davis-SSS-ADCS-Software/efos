//
//    FILE: AD5204_demo.ino
//  AUTHOR: Rob Tillaart
// PURPOSE: demo
//    DATE: 2020-07-24
//     URL: https://github.com/RobTillaart/AD520X


#include "AD520X.h"

#define DIRPIN 2

uint32_t start, stop;

//  select, reset, shutdown, data, clock
AD5204 pot(10, 255, 255, 8, 9);  // SW SPI

uint8_t pinmode = 0;
void setup()
{
  Serial.begin(115200);
  Serial.println(__FILE__);

  pot.begin(4);

  pinMode(DIRPIN, OUTPUT);

  Serial.println("\nDone...");
}


void loop()
{
    test_extremes();

    digitalWrite(DIRPIN, pinmode);
    

    //Switches directions after testing the extremes
    pinmode ^= 1;
    Serial.print(pinmode);

}

void test_extremes() //Tests extremes, so sets potentiometer at 0, then half, the full.
{
  Serial.println(__FUNCTION__);
  delay(10);

  // Off
  Serial.println("0");
  pot.setValue(0, 0);
  delay(2000);

  // Halfway
  Serial.println("127");
  pot.setValue(0, 127);
  delay(2000);

  // Full send
  Serial.println("255");
  pot.setValue(0, 255);
  delay(2000);
}
