#!/usr/bin/env python
# coding: utf8

import sys
import time
from random import random, randint
from typing import List

import RPi.GPIO as GPIO

# defines numbers of GPIO pins
GPIO.setmode(GPIO.BOARD)

# the mode chosen by the user
mode: int = int(sys.argv[1])

# defines led's
led0: int = 16
led1: int = 18
led2: int = 22
led3: int = 11
led4: int = 13
led5: int = 15

# list of all defined led's
led_list: List[int] = [led0, led1, led2, led3, led4, led5]

# defines GPIO pins as outputs
GPIO.setup(led0, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)


def running_light(runs: int = 3, wait: float = 0.1):
    while runs > 0:
        for led in led_list:
            GPIO.output(int(led), GPIO.HIGH)
            time.sleep(wait)
            GPIO.output(int(led), GPIO.LOW)
            time.sleep(wait)
        runs = runs - 1


def flickering_light(duration: int = 50):
    while duration > 0:
        random_led = randint(0, 5)
        GPIO.output(int(led_list[random_led]), GPIO.HIGH)
        time.sleep(random())
        GPIO.output(int(led_list[random_led]), GPIO.LOW)
        duration = duration - 1


if __name__ == '__main__':
    if mode == 1:
        running_light()
    elif mode == 2:
        flickering_light()
    else:
        sys.stdout.write("Please choose a mode between 1 and 2.")
    GPIO.cleanup()
