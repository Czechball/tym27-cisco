#include <FastLED.h>

//definice pinu atd.

#define LED_PIN 5
#define NUM_LEDS  15
#define BRIGHTNESS  32

#define DT  2
#define CLK 3

#define NUM_DISPLAYS 4

// array se vsemi led
CRGB leds[NUM_LEDS];

// pozice obrazovky/"hodnoty"
volatile int ledPosition = 0;

// "obrazovky"/hodnoty ktere led pasek zobrazuje
enum displays {
  trimr = 0,
  foto = 1,
  thermo = 2,
  analog = 3
};

int DTLastState;  
int lastClkState = digitalRead(CLK);

unsigned long lastInterruptTime = 0;
unsigned long textOutTimeLast = 0;

// interrupt rutina
void isr() {

  int currentClkState = digitalRead(CLK);
  unsigned long interruptTime = millis();

  // prepinani obrazovky encoderem, bounctime 50

  if (interruptTime - lastInterruptTime > 50) {

    if(currentClkState != lastClkState) {

      if (digitalRead(DT) != currentClkState) {

        if (ledPosition == 0)
          ledPosition = NUM_DISPLAYS-1;
        else
          ledPosition--;

      } else {

        if (ledPosition == NUM_DISPLAYS - 1)
          ledPosition = 0;
        else
          ledPosition++;

      }
      lastClkState = currentClkState;

      updateDisplay();    
    }
    lastInterruptTime = interruptTime;
  }
  
  
}

//update ledek
void updateDisplay() {
  reset();
  switch (ledPosition) {
    case trimr:
      display(68, CRGB::Green, A0);
      break;
    case foto:
      display(68, CRGB::Yellow, A1);
      break;
    case thermo:
        display(68, CRGB::Blue, A2);
      break;
    case analog:
        display(68, CRGB::Red, A3);
      break;
    default:
      display(68, CRGB::Green, A0);
      break;
  }
  FastLED.show();
}

void reset() {
   //reset vsech ledek
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CRGB::Black;
  }
}

//zobrazovani hodnoty na ledky
void display(int divideBy, CRGB color, int pin) {
  int to_light = analogRead(pin)/divideBy;
  for (int i = 0; i < to_light; i++) {
    leds[i] = color;
  }
}

void outStatus() {
  Serial.print("Potenciometr: ");
  Serial.println(analogRead(A0));
  Serial.print("Fotorezistor: ");
  Serial.println(analogRead(A1));
  Serial.print("Termorezistor: ");
  Serial.println(analogRead(A2));
  Serial.print("TMP36: ");
  Serial.println(analogRead(A3));
  Serial.println("---------------------");
}

void setup()
{
   
  Serial.begin(9600);

  FastLED.addLeds<NEOPIXEL, LED_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  pinMode(DT, INPUT);
  pinMode(CLK, INPUT);

  //pridani interruptu
  attachInterrupt(digitalPinToInterrupt(DT), isr, CHANGE);

}

void loop()
{

  // vypysuje pouze +- kazdou sekundu, ale ledky updatuje kazdych 200ms

  unsigned long textOutCurrent = millis();
  if (textOutCurrent - textOutTimeLast > 1000) {
    outStatus();
    textOutTimeLast = textOutCurrent;
  } 

  delay(200);
  updateDisplay();

}