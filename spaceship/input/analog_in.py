from ..base_process import BaseProcess
from time import sleep
from random import randrange


class AnalogIn(BaseProcess):

    def __init__(self, logger=None, quit_flag=None):
        super(AnalogIn, self).__init__(logger=logger, quit_flag=quit_flag)

    def run(self):
        dummy_1 = 0.0

        while not self.quit():
            dummy_1 += randrange(-100, 100) / 1000
            dummy_1 = dummy_1 % 100
            self.outgoing.put(('analog_1', dummy_1))
            sleep(0.1)
