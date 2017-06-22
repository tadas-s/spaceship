import multiprocessing as mp
from multiprocessing import Process, Value
import logging
from time import sleep
import readline
import atexit
import os
from .display import Display

class DummyProcess(Process):
    def __init__(self, logger=None, quit_flag=None):
        self.logger = logger
        self.quit = quit_flag
        super(DummyProcess, self).__init__()

    def run(self):
        while not self.quit.value:
            self.logger.info("Hello world!")
            sleep(1)

def main(args=None):
    mp.log_to_stderr()
    logger = mp.get_logger()
    logger.setLevel(logging.INFO)

    histfile = os.path.join(os.path.expanduser("~"), ".spaceship_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass
    atexit.register(readline.write_history_file, histfile)

    logger.info("Hello world!")

    q = Value('i', 0)

    p = Display(logger=logger, quit_flag=q)
    p.start()

    cmd = None
    while cmd != 'quit':
        cmd = input('--> ')
        print("Command: %s" % cmd)

    q.value = 1
    p.join()

    logger.info("I'm done here.")

if __name__ == "__main__":
    main()
