from machine import Pin, PWM
from utime import sleep
import random

# Set GPIO pin for audio output
buzzer = PWM(Pin(2))


def play(freq, duty=1000):
    # Set maximum volume
    buzzer.duty_u16(duty)
    # Play tone
    buzzer.freq(freq)


def stop():
    # Set minimum volume
    buzzer.duty_u16(0)


def test0():
    play(523, 32768)


# play(65)
# tone [d32768, f523]


def test1():
    start_value = random.randint(250, 768)
    for i in range(50):
        play(start_value - i, 32768)
        sleep(0.01)

    stop()


def siren(repeat=1, length=90):
    start_value = random.randint(500, 1000)
    for _ in range(repeat):
        for i in range(-length, length):
            play(start_value + abs(i), 32768)
            sleep(0.01)

    stop()
