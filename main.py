#!/usr/bin/env python
# coding: utf8

import time
from typing import List

import RPi.GPIO as GPIO

# defines numbers of GPIO pins
GPIO.setmode(GPIO.BOARD)

# defines led's
led0: int = 16
led1: int = 18
led2: int = 22
led3: int = 11
led4: int = 13
led5: int = 15

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
    GPIO.cleanup()


if __name__ == '__main__':
    running_light()
