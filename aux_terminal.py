import os
from subprocess import Popen, PIPE
import time

class AuxPipe():
    def __init__(self, title):
        self.PIPE_PATH = "/tmp/" + title

        if not os.path.exists(self.PIPE_PATH):
            os.mkfifo(self.PIPE_PATH)

        Popen(['xterm', '-e', 'tail -f %s' % self.PIPE_PATH])

    def write(self, message):
        with open(self.PIPE_PATH, "w") as p:
            p.write(message + "\n")