from time import sleep
from random import randrange
import board
import digitalio
import simon as si

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

restart = si.Button(board.BOOT0)

#%% test
while False:
    for i in range(4):
        event = buttons[i].button.check()
        if event == 1:
            buttons[i].press_feedback()
        if event == -1:
            buttons[i].release_feedback()
while False:
    event = restart.check()
    if event == -1:
        print('restart')
#%%
dt = 0.5
sequence = [randrange(4)]
while True: # each iteration is a round
    # play the sequence
    print('now playing')
    for i in sequence:
        sleep(dt * 0.1)
        buttons[i].press_feedback()
        sleep(dt)
        buttons[i].release_feedback()
    
    # user input and compare the sequence
    print('your turn')
    seq_ind = 0
    end_turn = False
    end = False
    while True: # FSM check state loop
        for i in range(4): # each iteration detects one Simon button
            event = buttons[i].button.check()
            if event == 1:
                buttons[i].press_feedback()
                print(i)
            if event == -1:
                buttons[i].release_feedback()
                if i == sequence[seq_ind]: # if correct
                    seq_ind += 1
                    if seq_ind == len(sequence): # if complete
                        print('good')
                        sleep(1)
                        sequence.append(randrange(4))
                        print(sequence)
                        end_turn = True
                else: # if wrong
                    end_turn = True
                    end = True
        if end_turn:
            dt *= 0.95
            break
    # reset and start a new
    if end:
        print('your score: ' + str(len(sequence) - 1))
        print('press D0 to restart')
        dt = 0.5
        sequence = [randrange(4)]
        while True:
            event = restart.check()
            if event == -1:
                break