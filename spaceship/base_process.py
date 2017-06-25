from multiprocessing import Process
from multiprocessing import Queue

class BaseProcess(Process):

    def __init__(self, logger=None, quit_flag=None):
        self.logger = logger
        self.quit_flag = quit_flag

        # Incoming messages queue from outside
        self.incoming = Queue()

        # Outgoing message queue to outside
        self.outgoing = Queue()

        super(BaseProcess, self).__init__()

    # Returns true if it's time to terminate
    def quit(self):
        return bool(self.quit_flag.value)
