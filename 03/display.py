#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
RPI + SSD1306 + BMP185 + DALLAS 18b20
Copyright (C) 2018 Vojtěch Hořánek

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import time
import requests
import os
import glob
import subprocess

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Adafruit_BMP.BMP085 as BMP085

import Image
import ImageDraw
import ImageFont

from RPi import GPIO
from time import sleep

# definovani portu pro encoder
ENCODER_CLK = 17
ENCODER_DT = 18
# definovani portu pro displej
DISPLAY_RST = 24
DISPLAY_DC = 23

# Inicializace rotacniho enkoderu
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCODER_CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENCODER_DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_clk_state = GPIO.input(ENCODER_CLK)

# Funkce vracici font pro psani na displej
def make_font(name, size):
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

font = make_font("/home/pi/noto.ttf", 20)
font_small = make_font("/home/pi/noto.ttf", 12)

# inicializace displeje
disp = Adafruit_SSD1306.SSD1306_128_64(
    rst=DISPLAY_RST, dc=DISPLAY_DC, 
    spi=SPI.SpiDev(0, 0, max_speed_hz=8000000)
    )

disp.begin()

disp.clear()
disp.display()

sensor = BMP085.BMP085()

spse = Image.open('spse.pnm').convert('1')
disp.image(spse)
disp.display()

WIDTH = disp.width
HEIGHT = disp.height

server_response = ""

screens = 8
current_screen = 1

# Funkce ktera vrati obsah soubory senzoru dallas
def read_temp():
    one_wire_dir = '/sys/bus/w1/devices/'
    device_dir = glob.glob(one_wire_dir + '28*')[0]
    device_file = device_dir + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Funkce ktera vrati teplotu senzoru dallas
def get_temp():
    lines = read_temp()
    # cekani dokud neni senzor dostupny
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp()
    equals_pos = lines[1].find('t=')
    # ziskani teploty se souboru
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

temp = get_temp()

def check_server():
    global server_response
    try:
        r = requests.head("https://nag-iot.zcu.cz/")
        server_response = u"Připojeno"
    except requests.ConnectionError:
        server_response = u"Nepřipojeno"

check_server()

# @param {string} primary Velky text
# @param {string} secondary Maly text
# @return {Image} novy Image s textem
# malovani na stejny draw bugovalo displej
def make_text_medium(primary, secondary):
    display_image = Image.new('1', (WIDTH, HEIGHT))
    image_draw = ImageDraw.Draw(display_image)
    image_draw.text((0, 0), secondary, font=font_small, fill=255)
    image_draw.text((0, 15), primary, font=font, fill=255)
    return display_image

# @param {Image} image image na kresleni
# zobrazuje tecky s pozici
def draw_position(image):
    INDICATOR_WIDTH = 5
    cur_pos_x = WIDTH-(INDICATOR_WIDTH*2*screens)
    image_draw = ImageDraw.Draw(image)
    for i in range(1, screens+1):
        mfill = 0

        if current_screen == i:
            mfill = 255

        image_draw.rectangle((
                             cur_pos_x-INDICATOR_WIDTH,   #x0
                             HEIGHT - (INDICATOR_WIDTH*2), #y0
                             cur_pos_x,                   #x1
                             HEIGHT - INDICATOR_WIDTH),    #y1
                             fill=mfill, outline=255)

        cur_pos_x += INDICATOR_WIDTH*2
    return image


# @param {Image} image novy image
def display_new_image(image):
    disp.clear()
    disp.image(image)
    disp.display()

# Vsechny obrazovky jsou definovany zde

def dallas_temp_screen():
    stri = u"{0:0.2f} °C".format(temp)
    image = make_text_medium(stri, "Teplota (dallas)")
    image = draw_position(image)
    display_new_image(image)

def date_screen():
    image = make_text_medium(time.strftime("%d.%m.%Y"), "Datum")
    image = draw_position(image)
    display_new_image(image)

def time_screen():
    image = make_text_medium(time.strftime("%H:%M:%S"), u"Čas")
    image = draw_position(image)
    display_new_image(image)

def server_screen():
    image = make_text_medium(server_response, "Server")
    image = draw_position(image)
    display_new_image(image)

def bmp_temp_screen():
    bmp_temp = "{0:0.2f}".format(sensor.read_temperature())
    image = make_text_medium(bmp_temp + u" °C", "Teplota (bmp180)")
    image = draw_position(image)
    display_new_image(image)

def bmp_pressure_screen():
    bmp_press = "{0:0.1f}".format(sensor.read_pressure()/100.0)
    image = make_text_medium(bmp_press + " hPa", "Tlak")
    image = draw_position(image)
    display_new_image(image)

def bmp_altitude_screen():
    bmp_alt = "{0:0.2f}".format(sensor.read_altitude())
    image = make_text_medium(bmp_alt + " m", u"Nadmořská výška")
    image = draw_position(image)
    display_new_image(image)

def kernel_screen():
    ver = subprocess.check_output(['uname', '-r']).split('-')[0]
    image = make_text_medium(ver, "Verze kernelu")
    image = draw_position(image)
    display_new_image(image)

# konec definice obrazovek

#interrup pro rotacni enkoder
def interrupt(channel):

    global current_screen
    global last_clk_state

    current_clk_state = GPIO.input(ENCODER_CLK)
    
    # jenom pokud se neco doopravdy stalo
    # pomaha to presnosti
    if current_clk_state != last_clk_state:
        if GPIO.input(ENCODER_DT) != current_clk_state:
            #toceni doprava
            if current_screen == screens:
                #prechod na prvni obtrazovku
                current_screen = 1
            else:
                current_screen += 1
        else:
            #toceni doleva
            if current_screen == 1:
                #prechod na posledni obrazovku
                current_screen = screens
            else:
                current_screen -= 1

        last_clk_state = current_clk_state
        switch_screen()

# prepinani obrazovek
def switch_screen():
    if current_screen == 1:
        time_screen()
    
    elif current_screen == 2:
        date_screen()
    
    elif current_screen == 3:
        server_screen()
    
    elif current_screen == 4:
        dallas_temp_screen()
    
    elif current_screen == 5:
        bmp_temp_screen()
    
    elif current_screen == 6:
        bmp_pressure_screen()
    
    elif current_screen == 7:
        bmp_altitude_screen()

    elif current_screen == 8:
        kernel_screen()

# pridavani interruptu na encoder
GPIO.add_event_detect(ENCODER_CLK, GPIO.BOTH, callback=interrupt, bouncetime=50)
switch_screen()

# nekonecna smycka ktera kazdych 5 vterin updatuje teplotu ze senzoru dallas
try:
    while True:

        temp = get_temp()
        check_server()
        sleep(5)

finally:
    GPIO.cleanup()