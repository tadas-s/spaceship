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

        bus1 = IoPi(bus, 0x20)
        bus1.set_port_direction(0, 0xFF)
        bus1.set_port_direction(1, 0xFF)
        bus1.set_port_pullups(0, 0xFF)
        bus1.set_port_pullups(1, 0xFF)

        bus2 = IoPi(bus, 0x21)
        bus2.set_port_direction(0, 0xFF)
        bus2.set_port_direction(1, 0xFF)
        bus2.set_port_pullups(0, 0xFF)
        bus2.set_port_pullups(1, 0xFF)

        # set initial values to something unusual to trigger
        # readout messages on startup
        pins = [
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None
        ]

        while not self.quit():
            for port in range(0, 16):
                pin = bus1.read_pin(port + 1)

                if pins[port] != pin:
                    pins[port] = pin
                    self.outgoing.put(('digital_%i' % port, pin))
                    self.logger.debug('digital_%i=%i' % (port, pin))

            for port in range(0, 16):
                pin = bus2.read_pin(port + 1)

                if pins[port + 16] != pin:
                    pins[port + 16] = pin
                    self.outgoing.put(('digital_%i' % (port + 16), pin))
                    self.logger.debug('digital_%i=%i' % ((port + 16), pin))

            sleep(0.1)
