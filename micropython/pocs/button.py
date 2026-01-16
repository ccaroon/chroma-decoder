from machine import Pin, PWM
from utime import sleep
import random

# Set GPIO pin for audio output
buzzer = PWM(Pin(15))


def play_tone(frequency):
    # Set maximum volume
    buzzer.duty_u16(1000)
    # Play tone
    buzzer.freq(frequency)


def be_quiet():
    # Set minimum volume
    buzzer.duty_u16(0)


## Set GPIO pins to use for switches
switch_1 = Pin(2, Pin.IN, Pin.PULL_DOWN)
switch_2 = Pin(3, Pin.IN, Pin.PULL_DOWN)
switch_3 = Pin(4, Pin.IN, Pin.PULL_DOWN)
## Infinite loop
while True:
    ## Continuous tone
    if switch_1.value():
        # Set tone frequency
        play_tone(65)
        ## Fast falling tone
    elif switch_2.value():
        # Set a random starting frequency
        start_value = random.randint(150, 1450)
        # Play falling frequencies
        for i in range(48):
            play_tone(start_value - i)
            sleep(0.001)
    ## Falling and rising glide
    elif switch_3.value():
        # Set a random starting frequency
        start_value = random.randint(120, 220)
        # Play repeatedly falling frequencies
        for i in range(-90, 90):
            play_tone(start_value + abs(i))
            sleep(0.008)
    else:
        be_quiet()
        sleep(0.05)
