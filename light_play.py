#!/usr/bin/env python
# encoding: utf8
# module: light_play

"""
This module provides some simple functions for showing
light animations on a Raspberry Pi.

Functions:

knight_rider_light() -- a light running from one side to the other and back
flickering_light() -- the LEDs flicker randomly
clapping_light() -- two lights running from the outer LEDs to the inner ones
"""

import sys
import time
from random import random, randint
from typing import List

import RPi.GPIO as GPIO

# defines how the GPIO pins are count
GPIO.setmode(GPIO.BOARD)
# the mode chosen by the user
mode: int = int(sys.argv[1])
# defines to which GPIO pins the LEDs are connected
led0: int = 16
led1: int = 18
led2: int = 22
led3: int = 11
led4: int = 13
led5: int = 15
# list of all defined LEDs
led_list: List[int] = [led0, led1, led2, led3, led4, led5]
# defines GPIO pins as outputs
GPIO.setup(led0, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)
GPIO.setup(led5, GPIO.OUT)


def knight_rider_light(runs: int = 10, wait: float = 0.1):
    """A light running from one side to the other and back.

    It looks like the light of the "Knight Rider".

    :parameter runs int, optional Describes how often the light should
    run from one site to the other. (default is 10)
    :parameter wait float, optional Describes how many seconds
    a led would shine. (default is 0.1)
    """
    while runs > 0:
        for led in led_list:
            GPIO.output(int(led), GPIO.HIGH)
            time.sleep(wait)
            GPIO.output(int(led), GPIO.LOW)
            time.sleep(wait)
        led_list.reverse()
        runs = runs - 1


def flickering_light(duration: int = 50):
    """The LEDs flicker randomly.

    It looks like a little fire.

    :parameter duration int, optional Describes how often
    the LEDs would flash. (default is 50)
    """
    while duration > 0:
        random_led = randint(0, 5)
        GPIO.output(int(led_list[random_led]), GPIO.HIGH)
        time.sleep(random())
        GPIO.output(int(led_list[random_led]), GPIO.LOW)
        duration = duration - 1


def clapping_light(runs: int = 10, wait: float = 0.1, invert: bool = False):
    """Two lights running from the outer LEDs to the inner ones.

    If invert is True they would start at the inner LEDs running to the
    outer ones.

    :parameter runs int, optional Describes how often the lights should
    run from one site to the other. (default is 10)
    :parameter wait float, optional Describes how many seconds
    a LED would shine. (default is 0.1)
    :parameter invert bool, optional Describes if the flashing lights
    should start at the outer or the inner LEDs. (default is False)
    """
    # splitting the list of all LEDs in outer, middle and inner LEDs
    outer_led: List[int] = [led_list[0], led_list[5]]
    middle_led: List[int] = [led_list[1], led_list[4]]
    inner_led: List[int] = [led_list[2], led_list[3]]
    # holds the single LED pairs starting with outer LEDs at index 0
    led_pairs: List[List] = [outer_led, middle_led, inner_led]

    while runs > 0:
        if not invert:
            # starts flashing with outer LEDs
            for pair in led_pairs:
                GPIO.output(pair, GPIO.HIGH)
                time.sleep(wait)
                GPIO.output(pair, GPIO.LOW)
                time.sleep(wait)
            led_pairs.reverse()
        else:
            # starts flashing with inner LEDs
            led_pairs.reverse()
            for pair in led_pairs:
                GPIO.output(pair, GPIO.HIGH)
                time.sleep(wait)
                GPIO.output(pair, GPIO.LOW)
                time.sleep(wait)
        runs = runs - 1


if __name__ == '__main__':
    if mode == 1:
        knight_rider_light()
    elif mode == 2:
        flickering_light()
    elif mode == 3:
        clapping_light()
    else:
        sys.stdout.write("Please choose a mode between 1 and 3.")
    GPIO.cleanup()
