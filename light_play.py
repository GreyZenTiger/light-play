#!/usr/bin/env python
# encoding: utf8
# module: light_play

"""
This module provides some simple functions for showing
light animations on a Raspberry Pi.

Functions:

create_config() -- creates config.ini if it's not existing
load_config() -- loads all variables from config.ini
knight_rider_light() -- a light running from one side to the other and back
flickering_light() -- the LEDs flicker randomly
clapping_light() -- two lights running from the outer LEDs to the inner ones
"""

import os.path
import sys
import time
from configparser import ConfigParser
from random import random, randint
from typing import List

import RPi.GPIO as GPIO

# get configparser object
config = ConfigParser()
config.read('config.ini')
# list of all defined LEDs
led_list: List[int] = []
# defines how the GPIO pins are count
GPIO.setmode(GPIO.BOARD)
# the mode chosen by the user
mode: int = int(sys.argv[1])


def create_config():
    """Creates the config.ini file if it's not existing."""
    # check if config.ini exists
    if not os.path.isfile('config.ini'):
        # predefine content of config.ini
        config['LedPosition'] = {
            'led0': '16', 'led1': '18', 'led2': '22',
            'led3': '11', 'led4': '13', 'led5': '15'
        }
        # create config.ini
        with open('config.ini', 'w') as conf:
            config.write(conf)


def load_config():
    """Loads all variables from config.ini file."""
    global led_list
    # load led positions from config.ini
    for key in config['LedPosition']:
        led_list.append(config.getint('LedPosition', key))
    # defines used GPIO pins as outputs
    for led in led_list:
        GPIO.setup(led, GPIO.OUT)


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
        # chooses a random index
        random_index = randint(0, 5)
        # flash random LED
        GPIO.output(int(led_list[random_index]), GPIO.HIGH)
        time.sleep(random())
        GPIO.output(int(led_list[random_index]), GPIO.LOW)
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
    left_index: int = 0
    right_index: int = len(led_list) - 1
    # holds the single LED pairs starting with outer LEDs at index 0
    led_pairs: List[List] = []
    # splitting the list of all LEDs in pairs from outer to inner LEDs
    while left_index <= right_index:
        led_pairs.append([led_list[left_index], led_list[right_index]])
        left_index = left_index + 1
        right_index = right_index - 1
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
    create_config()
    load_config()
    if mode == 1:
        knight_rider_light()
    elif mode == 2:
        flickering_light()
    elif mode == 3:
        clapping_light()
    else:
        sys.stdout.write("Please choose a mode between 1 and 3.")
    # cleanup the used GPIO pins
    GPIO.cleanup(led_list)
