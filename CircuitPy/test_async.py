# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import asyncio
import board
import digitalio
import simon as si
from random import random

buzzer = si.Buzzer(pin=board.D13)

class SimonButton:
    def __init__(self, led_pin, button_pin, freq):
        self.led = digitalio.DigitalInOut(led_pin)
        self.led.direction = digitalio.Direction.OUTPUT
        self.button = si.Button(button_pin)
        self.freq = freq
    def press_feedback(self):
        buzzer.sound(self.freq)
        self.led.value = True
    def release_feedback(self):
        buzzer.mute()
        self.led.value = False


buttons = [
    SimonButton(board.A1, board.D12, 392),
    SimonButton(board.A4, board.D5, 523),
    SimonButton(board.A2, board.A0, 784),
    SimonButton(board.A3, board.A5, 659),
]

async def feedback(button):  # Don't forget the async!
    while True:
        event = button.button.check()
        if event == 1:
            button.press_feedback()
        if event == -1:
            button.release_feedback()
        await asyncio.sleep(0.1 * random())


async def main():  # Don't forget the async!
    await asyncio.gather(*[
        asyncio.create_task(feedback(button))
        for button in buttons
    ])


asyncio.run(main())
