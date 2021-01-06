#!/usr/bin/env python3

import time
from ev3dev2.motor import (LargeMotor, MediumMotor, OUTPUT_B, OUTPUT_C,
                           OUTPUT_D, SpeedPercent)
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, ColorSensor


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


def main():
    printer = LegoPrinter(OUTPUT_C, OUTPUT_D, OUTPUT_B, INPUT_3, INPUT_4)
    printer.feedIn()
    printer.feedOut()


if __name__ == "__main__":
    main()
