  #include "DFRobot_PH.h"
  #include <EEPROM.h>
  #include <Wire.h>
  #include <LiquidCrystal_I2C.h>
  #include <Adafruit_HTU21DF.h>
  
  #define PH_PIN A1
  float voltage, phValue, temperature;
  DFRobot_PH ph;
  
  Adafruit_HTU21DF htu = Adafruit_HTU21DF();
  
  LiquidCrystal_I2C lcd(0x27, 16, 2);
  
  // New variables for the relay channels
  const int pHDOWN = 8;    // Relay channel for pH DOWN pump (connected to digital pin 11)
  const int pHUP = 9;      // Relay channel for pH UP pump (connected to digital pin 10)
  
  void setup() {
    Serial.begin(115200);
    lcd.init();
    lcd.backlight();
    ph.begin();
    htu.begin();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("This is a demo of Automated Hydroponics System");
    delay(3000);
  
    // Configure pin modes for the relay channels
    pinMode(pHDOWN, OUTPUT);
    pinMode(pHUP, OUTPUT);
    digitalWrite(pHDOWN, LOW);     // Turn off the pH DOWN pump relay initially
    digitalWrite(pHUP, LOW);       // Turn off the pH UP pump relay initially
  }
  
  void loop() {
    static unsigned long timepoint = millis();
    if (millis() - timepoint > 1000U) {
      timepoint = millis();
      temperature = htu.readTemperature();
      float humidity = htu.readHumidity();
      voltage = analogRead(PH_PIN) / 1024.0 * 5000;
      phValue = ph.readPH(voltage, temperature);
      Serial.print("temperature:");
      Serial.print(temperature, 1);
      Serial.print("^C  pH:");
      Serial.print(phValue, 2);
      Serial.print("  Humidity: ");
      Serial.print(humidity, 2);
      Serial.print("%");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Temp: ");
      lcd.print(temperature, 1);
      lcd.print(" C");
      lcd.setCursor(0, 1);
      lcd.print("pH: ");
      lcd.print(phValue, 2);
      lcd.setCursor(0, 2);
      lcd.print("Humidity: ");
      lcd.print(humidity, 3);
      lcd.print(" %");
  
      // Algorithm to control the pH pumps
      if (phValue > 7.0) {
        digitalWrite(pHDOWN, HIGH);  // Turn on the pH DOWN pump relay
        digitalWrite(pHUP, LOW);     // Turn off the pH UP pump relay
      } else if (phValue < 5.5) {
        digitalWrite(pHDOWN, LOW);   // Turn off the pH DOWN pump relay
        digitalWrite(pHUP, HIGH);    // Turn on the pH UP pump relay
      } else {
        digitalWrite(pHDOWN, LOW);   // Turn off the pH DOWN pump relay
        digitalWrite(pHUP, LOW);     // Turn off the pH UP pump relay
      }
    }
  
    ph.calibration(voltage, temperature);
  }
