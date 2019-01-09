# NAG-IoT
## Uzlabinsti ponici
## Instalace Raspbianu
Na RPi jsem instaloval Raspbian Lite z obrazu dostupneho na webu. Obraz byl kopirovan na microSD kartu ze sady ktera byla k pocitaci pripojena adapterem. Po pripojeni byla dostupna jako `/dev/sdd`. K kopirovani byl pouzit program `dd`. RPi dokumentace doporucuje nastaveni `bs=4M` a `conv=fsync`. Cely prikaz vypadal takto: `sudo dd if=~/Downloads/2018-11-13-raspbian-stretch.img of=/dev/sdd bs=4M conv=fsync`. Po dokonceni byla karta vyjmuta a vlozena to RPi. Pripojil jsem take monitor, mys a klavesnici. Pote RPi bez problemu nabootoval. Pro prihlaseni jsem pouzil prednastaveny ucet `pi` s heslem `raspberry`. Pomoci konfiguracniho skriptu `raspi-config` jsem nastavil rozlozeni klavesnice, lokal, cas a pripojil zarizeni k wifi. Prikazy `sudo apt update` a `sudo apt upgrade` jsem updatoval vsechen software. Nasledne jsem instaloval graficke prostredi Xfce.

## Instalace Arduino IDE
Program Arduino IDE jsem instaloval na RPi se systemem Raspbian. Program jsem stahoval ze webu arduina jelikoz verze na repozitarich raspianu byla zastarala. Musel jsem stahnout variantu pro architekturu ARM. Stazeny soubor jsem rozbalil prikazem `tar -xf arduino-1.8.8-linuxarm.tar.xz`. Ve nove vznikle slozne pak byl script `install.sh`. Po vykonani scriptu se program integroval do grafickeho prostredi. Ke konci jsem jeste instaloval ESP8266 core pro Arduino IDE. Stacilo v nastaveni do pole `Additional Board Manager` napsat `http://arduino.esp8266.com/stable/package_esp8266com_index.json` a v `Tools > Boards > Board menu` vybrat `install esp8266 platform`.

## Použité knihovny
[Arduino core for ESP8266 WiFi chip](https://github.com/esp8266/Arduino)

## Použité zdroje
[Raspbian](https://www.raspberrypi.org/downloads/raspbian/)

[Instalace raspbianu z linuxu](https://www.raspberrypi.org/documentation/installation/installing-images/linux.md)

[raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

[Arduino IDE](https://www.arduino.cc/en/main/software)
