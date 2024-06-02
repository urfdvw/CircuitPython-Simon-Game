from time import sleep
from random import randrange
import board
import digitalio
import displayio
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
import simon as si
from connected_variables import ConnectedVariables

# def connected variables
cv = ConnectedVariables()
cv.define('restart', False)
cv.define('info', '')
cv.update()

# peripheral
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

restart_btn = si.Button(board.BOOT0)

big_font_file = "/OCRA_big.pcf"
big_font = bitmap_font.load_font(big_font_file)
display = board.DISPLAY
display.rotation = 180

group = displayio.Group()
text = bitmap_label.Label(big_font, text="Hi", x=0, y=15, color=0xFF88FF)
group.append(text)
display.show(group)

#%% test
while False:
    for i in range(4):
        event = buttons[i].button.check()
        if event == 1:
            buttons[i].press_feedback()
        if event == -1:
            buttons[i].release_feedback()
while False:
    event = restart_btn.check()
    if event == -1:
        print('restart')
#%%
dt = 0.5
sequence = [randrange(4)]

def info(s):
    cv.write('info', s)
    text.text = s
    
while True: # each iteration is a round
    # play the sequence
    # print('now playing')
    info('now playing')
    for i in sequence:
        sleep(dt * 0.1)
        buttons[i].press_feedback()
        sleep(dt)
        buttons[i].release_feedback()
    
    # user input and compare the sequence
    # print('your turn')
    info('your turn')
    seq_ind = 0
    end_turn = False
    end = False
    while True: # FSM check state loop
        for i in range(4): # each iteration detects one Simon button
            event = buttons[i].button.check()
            if event == 1:
                buttons[i].press_feedback()
                # print(i)
            if event == -1:
                buttons[i].release_feedback()
                if i == sequence[seq_ind]: # if correct
                    seq_ind += 1
                    if seq_ind == len(sequence): # if complete
                        # print('good')
                        info('good')
                        sleep(1)
                        sequence.append(randrange(4))
                        # print(sequence)
                        end_turn = True
                else: # if wrong
                    end_turn = True
                    end = True
        if end_turn:
            dt *= 0.95
            break
    # reset and start a new
    if end:
        text.text = 'your score:\n' + str(len(sequence) - 1) + '\nD0: restart'
        cv.write('info', 'your score: ' + str(len(sequence) - 1) + '. Press "Restart" button to restart.')
        dt = 0.5
        sequence = [randrange(4)]
        last_restart = False
        while True:
            # based on button
            event = restart_btn.check()
            if event == -1:
                break
            # based on CV
            cur_restart = cv.read('restart')
            if not cur_restart and last_restart:
                break
            last_restart = cur_restart