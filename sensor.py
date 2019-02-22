#!/usr/bin/env python
IO = {
    'DIGITAL': {
        'read': 'digitalRead',
        'write': 'digitalWrite',
    },
    'ANALOG': {
        'read': 'analogRead',
        'write': 'analogWrite',
    }
}


def get_pin(pin, pininstance):
    return pininstance if pin is None else pin


class Sensor(object):
    """ Sensor
    """
    DEFAULT_PIN = 13

    def __init__(self, board,
                 pin=DEFAULT_PIN,
                 mode='DIGITAL',
                 default_analog_value=0):
        self._pin = pin
        self._mode = IO.get(mode, 'DIGITAL')
        self.default_analog_value = default_analog_value
        self.board = board

    @property
    def mode(self, ):
        return self.__mode

    @mode.setter
    def _mode(self, mode):
        if getattr(self, '__mode', None) is not None:
            raise NotImplementedError("Cannot change mode options")
        self.__mode = mode

    @property
    def pin(self, ):
        return self._pin

    def setMode(self, mode="OUTPUT", pin=None):
        self.board.pinMode(get_pin(pin, self.pin), mode)

    def write(self, value, pin=None):
        getattr(self.board, self.mode['write'])(get_pin(pin, self.pin), value)

    def read(self, pin=None):
        return getattr(self.board, self.mode['read'])(get_pin(pin, self.pin))
