from machine import Pin, PWM
from utime import sleep
import random

# Set GPIO pin for audio output
buzzer = PWM(Pin(2))


def play_tone(frequency):
    # Set maximum volume
    buzzer.duty_u16(1000)
    # Play tone
    buzzer.freq(frequency)


def be_quiet():
    # Set minimum volume
    buzzer.duty_u16(0)


# play_tone(65)


def thing1():
    start_value = random.randint(150, 1450)
    for i in range(48):
        play_tone(start_value - i)
        sleep(0.001)


def thing2():
    start_value = random.randint(120, 220)
    for i in range(-90, 90):
        play_tone(start_value + abs(i))
        sleep(0.008)
