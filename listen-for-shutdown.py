#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import time
from time import sleep

button_gpio=3
relay_gpio=4

short_press=0.5
long_press=10

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(relay_gpio, GPIO.OUT)

def main():
  relay_state=False
  GPIO.output(relay_gpio, relay_state)
  while True:
    GPIO.wait_for_edge(button_gpio, GPIO.FALLING)
    counter = 0
    while GPIO.input(button_gpio) == 0 and counter < long_press:
      time.sleep(0.1)
      counter = round(counter + 0.1, 1)
      print('Shutdown button is pressed ' + str(counter))
    if counter >= long_press:
      print('Shutting down')
      subprocess.call(['shutdown', '-h', 'now'], shell=False)
    elif counter >= short_press:
      relay_state = not relay_state
      print('Changing relay state to: ' + str(relay_state))
      GPIO.output(relay_gpio, relay_state)

if __name__ == '__main__':
  main()
