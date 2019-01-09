# NAG-IoT
## Úžlabinští poníci

## A - Ovládání portu ve výstupním režimu
LED dioda bliká pomocí ovládání napětí na GPIO portu. Totéž platí pro bzučák.
Aplikace se spouští příkazy `$ python LED.py` pro LED diodu a `$ python buzzer.py` pro bzučák.

### Použité součástky
#### Ovládání LED diody
| Součástka | Počet |
| -------- | -------- |
| Rezistor 220 Ω | 1 |
| LED Dioda | 1 |
| Raspberry Pi 3 mobdel B | 1 |
| Breadboard | 1 |
| Spojovací dráty | 2 |
#### Ovládání bzučáku
| Součástka | Počet |
| -------- | -------- |
| Bzučák | 1 |
| Raspberry Pi 3 mobdel B | 1 |
| Breadboard | 1 |
| Spojovací dráty | 2 |
### Zapojení
#### LED Dioda
| Součástka | GPIO |
| -------- | -------- |
| LED Dioda + Rezistor | 21 |
#### Bzučák
| Součástka | GPIO |
| -------- | -------- |
| Bzučák | 21 |

## B - Řízení výkonu na GPIO portu pomocí PWM
LED dioda mění jas dle zadaného výkonu, v tomto případě roste z minima do maxima a poté zpět.
Aplikace se spouští pomocí `$ python LED_PWM.py`
### Použité součástky
| Součástka | Počet |
| -------- | -------- |
| Rezistor 220 Ω | 1 |
| LED Dioda | 1 |
| Raspberry Pi 3 mobdel B | 1 |
| Breadboard | 1 |
| Spojovací dráty | 2 |
### Zapojení
| Součástka | GPIO |
| -------- | -------- |
| LED Dioda + Rezistor | 21 |

## C - Ovládání RGB LED diody pomocí PWM
LED dioda mění barvy pomocí míchání červené, zelené a modré ovládaných pomocí PWM.
Aplikace se spouští pomocí `$ python RGB_PWM.py`
### Použité součástky
| Součástka | Počet |
| -------- | -------- |
| Rezistor 220 Ω | 1 |
| LED Dioda | 1 |
| Raspberry Pi 3 mobdel B | 1 |
| Breadboard | 1 |
| Spojovací dráty | 4 |
### Zapojení
| Součástka | GPIO |
| -------- | -------- |
| LED Dioda (R) | 18 |
| LED Dioda (G) | 13 |
| LED Dioda (B) | 19 |
## D - Detekce vstupu na portu
Aplikace vypíše textový výstup po každé, když je tlačítko zmáčknuto. Aplikace se spouští pomocí `$ python Button.py`
### Použité součástky
| Součástka | Počet |
| -------- | -------- |
| Tlačítko | 1 |
| Raspberry Pi 3 mobdel B | 1 |
| Breadboard | 1 |
| Spojovací dráty | 2 |
### Zapojení
| Součástka | GPIO |
| -------- | -------- |
| Tlačítko | 13 |
## Použité knihovny
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/)
## Použité zdroje
[RPi - PWM](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/)