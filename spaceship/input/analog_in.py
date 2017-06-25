from ..base_process import BaseProcess
from time import sleep
from ADCPi.ABE_helpers import ABEHelpers
from ADCPi.ABE_ADCPi import ADCPi


class AnalogIn(BaseProcess):

    def __init__(self, logger=None, quit_flag=None):
        super(AnalogIn, self).__init__(logger=logger, quit_flag=quit_flag)

    def run(self):
        i2c_helper = ABEHelpers()
        bus = i2c_helper.get_smbus()

        if not bus:
            self.logger.warn('No i2c bus? Quitting.')
            return

        adc = ADCPi(bus, 0x6e, 0x6f, 12)

        voltages = [
            adc.read_voltage(1),
            adc.read_voltage(2),
            adc.read_voltage(3),
            adc.read_voltage(4),
            adc.read_voltage(5),
            adc.read_voltage(6),
            adc.read_voltage(7),
            adc.read_voltage(8)
        ]

        while not self.quit():
            for port in range(0, 8):
                voltage = adc.read_voltage(port + 1)

                if voltages[port] != voltage:
                    voltages[port] = voltage
                    self.outgoing.put(('analog_%i' % port, voltage))
                    self.logger.debug('analog_%i=%f' % (port, voltage))

            sleep(0.02)
