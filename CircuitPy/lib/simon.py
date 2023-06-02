import board

import pwmio
class Buzzer:
    def __init__(self, pin, freq=880):
        self.buzzer = pwmio.PWMOut(pin, variable_frequency=True)
        self.buzzer.duty_cycle = 0
        self.on = False
        self.freq = freq
    def show(self):
        self.buzzer.frequency = self.freq
        self.buzzer.duty_cycle = 32768 if self.on else 0
    def set_freq(self, freq):
        if freq == 0:
            self.on = False
        else:
            self.freq = freq
        self.show()
    def sound(self, freq=None):
        self.on = True
        if freq is not None:
            self.set_freq(freq)
        self.show()
    def mute(self):
        self.on = False
        self.show()
    def beep(self, freq=None, duration=0.01):
        self.sound(freq)
        sleep(duration)
        self.mute()
        
import digitalio
class Button:
    def __init__(self, pin):
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.current = False
        self.last = False

    def check(self):
        # compute output
        self.current = not self.button.value
        out = None
        if self.current and (not self.last):
            out = 1 # press edge
        elif (not self.current) and self.last:
            out = -1 # release edge
        elif self.current and self.last:
            out = 2 # hold
        else: # idle
            out = 0
        self.last = self.current
        return out