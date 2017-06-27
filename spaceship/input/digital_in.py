from ..base_process import BaseProcess
from time import sleep
from IOPi.ABE_helpers import ABEHelpers
from IOPi.ABE_IoPi import IoPi


class DigitalIn(BaseProcess):

    def __init__(self, logger=None, quit_flag=None):
        super(DigitalIn, self).__init__(logger=logger, quit_flag=quit_flag)

    def run(self):
        i2c_helper = ABEHelpers()
        bus = i2c_helper.get_smbus()

        if not bus:
            self.logger.warn('No i2c bus? Quitting.')
            return

        digital_in = IoPi(bus, 0x20)
        digital_in.set_port_direction(0, 0xFF)
        digital_in.set_port_pullups(0, 0xFF)

        # set initial values to something unusual to trigger
        # readout messages on startup
        pins = [
            None, None, None, None, None, None, None, None
        ]

        while not self.quit():
            for port in range(0, 8):
                pin = digital_in.read_pin(port + 1)

                if pins[port] != pin:
                    pins[port] = pin
                    self.outgoing.put(('digital_%i' % port, pin))
                    self.logger.debug('digital_%i=%i' % (port, pin))

            sleep(0.1)
