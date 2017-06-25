from .base_process import BaseProcess


# Routes messages from one multiprocess.Queue to multiple queues.
class MessageRouter(BaseProcess):

    def __init__(self, logger=None, quit_flag=None, routes={}):
        self.routes = routes
        super(MessageRouter, self).__init__(logger=logger, quit_flag=quit_flag)

    def run(self):
        while not self.quit():
            for source, destinations in self.routes.items():
                if not source.empty():
                    # single message at a time
                    message = source.get()
                    for destination in destinations:
                        destination.put(message)
