#!/usr/bin/env python3

import time
from ev3dev2.motor import (LargeMotor, MediumMotor, OUTPUT_B, OUTPUT_C,
                           OUTPUT_D, SpeedPercent)
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.stopwatch import StopWatch
from ev3dev2.button import Button


class LegoPrinter(object):

    calibrated = False
    # test pattern
    helloWorld = 'Hello World'

    def __init__(self, mpf_port, mpl_port, mph_port, cs_port, ts_port,
                 line_position=525, line_width=1050, letter_size=10,
                 letter_spacing=10):

        self.motor_paper_feed = LargeMotor(mpf_port)
        self.motor_pen_lift = MediumMotor(mpl_port)
        self.motor_pen_horizontal = LargeMotor(mph_port)
        self.color_sensor = ColorSensor(cs_port)
        self.touch_sensor = TouchSensor(ts_port)
        for i in [self.motor_paper_feed, self.motor_pen_lift,
                  self.motor_pen_horizontal, self.color_sensor,
                  self.touch_sensor]:
            assert i.connected
        self.btn = Button()
        self.lineposition = line_position
        self.linewidth = line_width
        self.lettersize = letter_size
        self.letterspacing = letter_spacing
        # dictionary connecting letters and printing methods
        self.letters = {'A': self.printA,
                        'B': self.printB,
                        'C': self.printC,
                        'D': self.printD,
                        'E': self.printE,
                        'F': self.printF,
                        'G': self.printG,
                        'H': self.printH,
                        'I': self.printI,
                        'J': self.printJ,
                        'K': self.printK,
                        'L': self.printL,
                        'M': self.printM,
                        'N': self.printN,
                        'O': self.printO,
                        'P': self.printP,
                        'Q': self.printQ,
                        'R': self.printR,
                        'S': self.printS,
                        'T': self.printT,
                        'U': self.printU,
                        'V': self.printV,
                        'W': self.printW,
                        'X': self.printX,
                        'Y': self.printY,
                        'Z': self.printZ,
                        ' ': self.printSpace
                        }

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

    def liftPen(self, speed):
        self.motor_pen_lift.on_for_degrees(speed=speed, degrees=180)
        self.motor_pen_lift.wait_until_not_moving()

    def movePaper(self, speed):
        # gear reduction in paper feed motor: 12 / 36
        self.motor_paper_feed.on_for_degrees(speed=speed,
                                             degrees=(36/12)*self.lettersize)
        self.motor_paper_feed.wait_until_not_moving()

    def movePen(self, speed):
        # gear reduction in pen horizontal motor: 12 / 36
        self.motor_pen_horizontal.on_for_degrees(
            speed=speed, degrees=(36/12)*self.letterspacing)
        self.motor_pen_horizontal.wait_until_not_moving()

    def carriageReturn(self):
        pass

    def manualPaperFeed(self, speed=100):
        while not self.btn.enter:
            if self.btn.up:
                self.motor_paper_feed.run_forever(speed_sp=-speed)
                while self.btn.up:
                    time.sleep(0.1)
                self.motor_paper_feed.stop()
            elif self.btn.down:
                self.motor_paper_feed.run_forever(speed_sp=speed)
                while self.btn.down:
                    time.sleep(0.1)
                self.motor_paper_feed.stop()

    def calibrate(self):
        while not self.btn.enter:
            if self.btn.right:
                self.motor_pen_horizontal.run_forever(speed_sp=100)
                while self.btn.right:
                    time.sleep(0.1)
                self.motor_pen_horizontal.stop()
            elif self.btn.left:
                self.motor_pen_horizontal.run_forever(speed_sp=-100)
                while self.btn.left:
                    time.sleep(0.1)
                self.motor_pen_horizontal.stop()
            elif self.btn.up:
                self.motor_pen_lift.run_forever(speed_sp=100)
                while self.btn.up:
                    time.sleep(0.1)
                self.motor_pen_lift.stop()
            elif self.btn.down:
                self.motor_pen_lift.run_forever(speed_sp=-100)
                while self.btn.down:
                    time.sleep(0.1)
                self.motor_pen_lift.stop()
        self.motor_pen_horizontal.reset()
        self.motor_pen_lift.reset()
        self.calibrated = True
        self.motor_pen_horizontal.on_to_position(position=self.lineposition,
                                                 speed=100)

    def printA(self):
        pass

    def printB(self):
        pass

    def printC(self):
        pass

    def printD(self):
        pass

    def printE(self):
        pass

    def printF(self):
        pass

    def printG(self):
        pass

    def printH(self):
        pass

    def printI(self):
        self.movePaper(-25)
        self.liftPen(-25)
        self.movePaper(25)
        self.liftPen(25)

    def printJ(self):
        pass

    def printK(self):
        pass

    def printL(self):
        pass

    def printM(self):
        pass

    def printN(self):
        pass

    def printO(self):
        pass

    def printP(self):
        pass

    def printQ(self):
        pass

    def printR(self):
        pass

    def printS(self):
        pass

    def printT(self):
        pass

    def printU(self):
        pass

    def printV(self):
        pass

    def printW(self):
        pass

    def printX(self):
        pass

    def printY(self):
        pass

    def printZ(self):
        pass

    def printSpace(self):
        pass

    def printerQueue(self, text):
        for letter in text:
            if letter in self.letters.keys():
                self.letters[letter]()


class Telegraph(object):

    MORSE_CODE = {'A': '.-',
                  'B': '-...',
                  'C': '-.-.',
                  'D': '-..',
                  'E': '.',
                  'F': '..-.',
                  'G': '--.',
                  'H': '....',
                  'I': '..',
                  'J': '.---',
                  'K': '-.-',
                  'L': '.-..',
                  'M': '--',
                  'N': '-.',
                  'O': '---',
                  'P': '.--.',
                  'Q': '--.-',
                  'R': '.-.',
                  'S': '...',
                  'T': '-',
                  'U': '..-',
                  'V': '...-',
                  'W': '.--',
                  'X': '-..-',
                  'Y': '-.--',
                  'Z': '--..',
                  '1': '.----',
                  '2': '..---',
                  '3': '...--',
                  '4': '....-',
                  '5': '.....',
                  '6': '-....',
                  '7': '--...',
                  '8': '---..',
                  '9': '----.',
                  '0': '-----',
                  ', ': '--..--',
                  '.': '.-.-.-',
                  '?': '..--..',
                  '/': '-..-.',
                  '-': '-....-',
                  '(': '-.--.',
                  ')': '-.--.-'}

    def __init__(self, ts_port):
        self.touch_sensor = TouchSensor(ts_port)
        assert self.touch_sensor.connected
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
                    elif self.morse_code and 1000 <= timer.value_ms < 2000:
                        if self.morse_code[-2:] != '  ':
                            self.morse_code += ' '
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
                    self.decode += list(self.MORSE_CODE.keys())[list(
                        self.MORSE_CODE.values()).index(text)]
                    text = ''
        return self.decode


def main():
    printer_parameter = {'mpf_port': OUTPUT_C,
                         'mph_port': OUTPUT_B,
                         'mpl_port': OUTPUT_D,
                         'cs_port': INPUT_3,
                         'ts_port': INPUT_4,
                         'line_position': 525,
                         'line_width': 1050,
                         'letter_size': 10,
                         'letter_spacing': 10}
    printer = LegoPrinter(**printer_parameter)
    # printer.feedIn()
    # printer.feedOut()
    printer.manualPaperFeed()
    # printer.calibrate()
    # telegraph = Telegraph(INPUT_4)
    # telegraph.sendMorseMessage()
    # telegraph.decodeMorseMessage(telegraph.morse_code)
    # print(telegraph.decode)
    # printer.liftPen(25)
    # printer.printI()
    # printer.printerQueue('I')


if __name__ == "__main__":
    main()
