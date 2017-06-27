import multiprocessing as mp
from multiprocessing import Value
import logging
import readline
import atexit
import os
import re
from .display import Display
from .input.analog_in import AnalogIn
from .input.digital_in import DigitalIn
from .message_router import  MessageRouter

def main(args=None):
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel((os.environ.get('LOG_LEVEL') or 'INFO').upper())

    histfile = os.path.join(os.path.expanduser("~"), ".spaceship_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass
    atexit.register(readline.write_history_file, histfile)

    logger.info("Hello world!")

    q = Value('i', 0)

    p1 = Display(logger=logger, quit_flag=q)
    p1.start()

    p2 = AnalogIn(logger=logger, quit_flag=q)
    p2.start()

    p3 = DigitalIn(logger=logger, quit_flag=q)
    p3.start()

    router_process = MessageRouter(
        logger=logger,
        quit_flag=q,
        routes={p2.outgoing: [p1.incoming]}
    )
    router_process.start()

    cmd = None
    while cmd != 'quit':
        cmd = input('--> ')

        if re.match('^analog_(\d+)=([\d]+(\.\d+)?)$', cmd):
            logger.info('Sending msg: ' + str((cmd.split("=")[0], float(cmd.split("=")[1]))))
            p1.incoming.put(
                (cmd.split("=")[0], float(cmd.split("=")[1]))
            )

    q.value = 1

    router_process.join()
    p3.join()
    p2.join()
    p1.join()

    logger.info("I'm done here.")

if __name__ == "__main__":
    main()
