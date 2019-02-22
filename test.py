#!/usr/bin/env python
import time
from functools import partial

from sensor import Sensor
from Arduino import Arduino


class KE008(Sensor):
    """
    Laser
    """
    def __init__(self, *args, **kwargs):
        super(KE008, self).__init__(*args, **kwargs)


class KY040(Sensor):
    CLOCKWISE = 0
    ANTICLOCKWISE = 1

    def __init__(self, board, *args, **kwargs):
        self.clock_pin = kwargs.pop('clock_pin')
        self.data_pin = kwargs.pop('data_pin')
        self.switch_pin = kwargs.pop('switch_pin')

        self.rotary_callback = kwargs.pop('rotary_callback')
        self.switch_callback = kwargs.pop('switch_callback')

        board.pinMode(self.clock_pin, 'INPUT')
        board.pinMode(self.data_pin, 'INPUT')
        board.pinMode(self.switch_pin, 'INPUT')
        super(KY040, self).__init__(board, *args, **kwargs)


    def _clock_callback(self):
        if self.read(self.clock_pin) == 0:
            data = self.read(self.data_pin)
            if data == 1:
                self.rotary_callback(self.ANTICLOCKWISE)
            else:
                self.rotary_callback(self.CLOCKWISE)

    def _switch_callback(self):
        if self.switch_pin is None:
            return

        if self.read(self.switch_pin) == 0:
            self.write(1, self.switch_pin)
            self.switch_callback()


def switch(laser):
    print('switch')
    value = laser.read()
    print('laser value (255)', value)
    if value <= 15:
        laser.write(255)
    if value >=15:
        laser.write(0)
    time.sleep(1)

def rotary(laser, wise):
    print('wise ->', wise)
    laser_value = laser.read()
    print('laser value: ', laser_value)
    if wise:
        laser_value += 20
        laser.write(laser_value)
    else:
        laser_value -= 20
        laser.write(laser_value)
    time.sleep(1)




if __name__ == '__main__':
    board = Arduino('9600', port='/dev/ttyACM0')
    laser = KE008(board, pin=11, mode='ANALOG')
    laser.setMode()

    power = 1
    laser.write(power)

    switcher = KY040(board, clock_pin=2, data_pin=7, switch_pin=8,
            rotary_callback=partial(rotary, laser),
            switch_callback=partial(switch, laser),
            )
    while True:
        switcher._switch_callback()
        switcher._clock_callback()
