#!/usr/bin/env python3

import time
from ev3dev2.motor import (LargeMotor, MediumMotor, OUTPUT_B, OUTPUT_C,
                           OUTPUT_D, SpeedPercent)
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.stopwatch import StopWatch


MORSE_CODE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
              'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
              'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
              'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
              'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
              'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---',
              '3': '...--', '4': '....-', '5': '.....', '6': '-....',
              '7': '--...', '8': '---..', '9': '----.', '0': '-----',
              ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
              '-': '-....-', '(': '-.--.', ')': '-.--.-'}


class LegoPrinter(object):

    def __init__(self, mpf_port, mpl_port, mph_port, cs_port, ts_port):

        self.motor_paper_feed = LargeMotor(mpf_port)
        self.motor_pen_lift = MediumMotor(mpl_port)
        self.motor_pen_horizontal = LargeMotor(mph_port)
        self.color_sensor = ColorSensor(cs_port)
        self.touch_sensor = TouchSensor(ts_port)

        self.lineposition = 525
        self.linewidth = 1050
        self.lettersize = 20
        self.textsize = 10

        self.helloworld = [7, 4, 11, 11, 14, 26, 22, 14, 17, 11, 3, 27]

        self.calibrated = False

    def feedOut(self, speed=100):
        self.motor_paper_feed.run_forever(speed_sp=speed)
        while self.color_sensor.reflected_light_intensity >= 4:
            time.sleep(0.1)
        self.motor_paper_feed.on_for_degrees(speed=SpeedPercent(30),
                                             degrees=720)
        self.motor_paper_feed.stop()

    def feedIn(self, speed=100):
        self.motor_paper_feed.run_forever(speed_sp=-speed)
        while self.color_sensor.reflected_light_intensity <= 4:
            time.sleep(0.1)
        self.motor_paper_feed.stop()


class Telegraph(object):

    def __init__(self, ts_port):
        self.touch_sensor = TouchSensor(ts_port)
        self.speaker = Sound()
        self.morse_code = ''
        self.decode = ''

    def sendMorseMessage(self):
        timer = StopWatch()
        morse_signal = False
        beep = None
        print('Ready to receive Morse Code!')
        while True:
            if self.touch_sensor.is_pressed:
                morse_signal = True
                timer.restart()
                beep = self.speaker.beep("-f 750 -l 31536000000", 1)
                self.touch_sensor.wait_for_released()
            else:
                if beep is not None:
                    beep.terminate()
                if morse_signal:
                    if timer.value_ms < 200:
                        self.morse_code += '.'
                    else:
                        self.morse_code += '-'
                    morse_signal = False
                    print(self.morse_code)
                else:
                    if self.morse_code and 600 <= timer.value_ms < 1000:
                        if self.morse_code[-1] != ' ':
                            self.morse_code += ' '
                            print(self.morse_code)
                    elif self.morse_code and 1000 <= timer.value_ms < 2000:
                        if self.morse_code[-2:] != '  ':
                            self.morse_code += ' '
                            print(self.morse_code)
                    elif self.morse_code and timer.value_ms > 5000:
                        break
        return self.morse_code

    def decodeMorseMessage(self, message):
        text = ''
        counter = 0
        for letter in message:
            if letter != ' ':
                counter = 0
                text += letter
            else:
                counter += 1
                if counter == 2:
                    self.decode += ' '
                else:
                    self.decode += list(MORSE_CODE.keys())[list(
                        MORSE_CODE.values()).index(text)]
                    text = ''
        return self.decode


def main():
    # printer = LegoPrinter(OUTPUT_C, OUTPUT_D, OUTPUT_B, INPUT_3, INPUT_4)
    # printer.feedIn()
    # printer.feedOut()
    telegraph = Telegraph(INPUT_4)
    telegraph.sendMorseMessage()
    telegraph.decodeMorseMessage(telegraph.morse_code)
    print(telegraph.decode)


if __name__ == "__main__":
    main()
