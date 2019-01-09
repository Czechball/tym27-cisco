# NAG-IoT
## Úžlabinští poníci 

Aplikace posílá na soutěžní server teplotu a tlak ze senzorů BMP180 a DALLAS 18B20. Data jsou zasílána v intervalu jedné minuty.

Aplikace se spouští pomocí `$ python teplota.py`

### Připojení pinů

|Zařízení|GPIO|
|--------|----|
|**BMP 180** SDA|2|
|BMP 180 SCL|3|
|**Dallas** DS18B20|4|

### Zdroje

[Dallas DS18B20](https://pimylifeup.com/raspberry-pi-temperature-sensor/)  

### Knihovny

[Adafruit BMP180](https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/using-the-adafruit-bmp-python-library)  
[RPi.GPIO](https://pypi.org/project/RPi.GPIO/)  
[Requests](http://docs.python-requests.org/en/master/)  

