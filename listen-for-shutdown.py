#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import time
from time import sleep

button_gpio=3
light_gpio=27
fan_gpio=22

short_press=0.1
long_press=10

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(light_gpio, GPIO.OUT)
GPIO.setup(fan_gpio, GPIO.OUT)

def main():
  while True:
    GPIO.wait_for_edge(button_gpio, GPIO.FALLING)
    counter = 0
    while GPIO.input(button_gpio) == 0 and counter < long_press:
      time.sleep(0.1)
      counter = round(counter + 0.1, 1)
      
      if counter >= long_press:
        print('Shutting down')
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
        return # Exit the script as the system is shutting down
      
      if int(counter * 10) % 10 == 0: # Print every second to keep logs clean
        print(f'Button held for: {counter}s')
      
    if counter >= short_press and counter < long_press:
      relay_state = not (GPIO.input(light_gpio) or GPIO.input(fan_gpio))
      print('Changing relay state to: ' + str(relay_state))
      GPIO.output(light_gpio, relay_state)
      GPIO.output(fan_gpio, relay_state)
      time.sleep(short_press)

if __name__ == '__main__':
  main()
