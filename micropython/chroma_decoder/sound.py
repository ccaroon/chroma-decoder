import time

from machine import PWM, Pin, Timer


class Sound:
    # A3
    __PIEZO_PIN = 28
    __ON = 32768
    __OFF = 0

    TONE_FREQ = (
        262,  # C4
        294,  # D4
        330,  # E4
        349,  # F4
        392,  # G4
        440,  # A4
        494,  # B4
    )

    def __init__(self):
        self.__timer = Timer()
        self.__speaker = PWM(Pin(self.__PIEZO_PIN))

    def play(self, freq):
        self.__speaker.duty_u16(self.__ON)
        self.__speaker.freq(freq)

    def stop(self, _=None):
        self.__speaker.duty_u16(self.__OFF)

    def tone(self, freq, duration):
        self.play(freq)
        self.__timer.init(
            period=duration,
            mode=Timer.ONE_SHOT,
            callback=self.stop,
        )

    def scale(self):
        for freq in self.TONE_FREQ:
            self.play(freq)
            time.sleep(0.5)

        self.stop()

    def drop(self, start_freq, duration):
        delta_freq = start_freq // duration
        for i in range(duration):
            freq = start_freq - (delta_freq * i)
            freq = max(freq, 10)
            self.play(freq)
            time.sleep(0.01)

        self.stop()

    def siren(self, start_value, repeat=1, length=175):
        for _ in range(repeat):
            for i in range(-length, length):
                self.play(start_value + abs(i))
                time.sleep(0.01)

        self.stop()
