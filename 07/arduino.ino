// Konstanty
const uint8_t pinPir = 5;
const uint8_t pinShake = A0;
const uint8_t pinTilt = 6;

const uint8_t ledPinRed = 2;
const uint8_t ledPinGreen = 3;
const uint8_t ledPinBlue = 4;

unsigned long lastPinGreen;

uint8_t lastPir, lastTilt;
    
void setup() {
  
    pinMode(pinPir, INPUT);
    pinMode(pinTilt, INPUT_PULLUP );

    pinMode(ledPinRed, OUTPUT);
    pinMode(ledPinGreen, OUTPUT);
    pinMode(ledPinBlue, OUTPUT);

    lastPir = digitalRead(pinPir);
    lastTilt = digitalRead(pinTilt);

}
    
void loop(){

    //kontrola PIR
    if(digitalRead(pinPir) == HIGH) {
        // pohyb
        if (lastPir != HIGH) {
            digitalWrite(ledPinBlue, HIGH);
            lastPir = HIGH;
        }
    } else {
        // bez pohybu
         if (lastPir != LOW) {
            digitalWrite(ledPinBlue, LOW);
            lastPir = LOW;
        }
    }

    //kontrola otresoveho senzoru
    // zmenou 800 na mensi se zvysi sensitivita
    if(analogRead(pinShake) >= 800) {
        digitalWrite(ledPinRed, HIGH);
    } else {
        digitalWrite(ledPinRed, LOW);
    }

    //kontrola polohoveho senzoru
    if(lastTilt != digitalRead(pinTilt)) {
        digitalWrite(ledPinGreen, HIGH);
        lastPinGreen = millis();
    } else {
        if (millis() - lastPinGreen >= 1000) {
            digitalWrite(ledPinGreen, LOW);
        }
    }
    
    lastTilt = digitalRead(pinTilt);


}