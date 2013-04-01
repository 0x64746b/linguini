import gtk
import multiprocessing
from multiprocessing import queues
import logging
import os
import readline
import signal
import sys


SIGNAL_NEW_CLIPBOARD_CONTENT = 'owner-change'

logger = logging.getLogger(__name__)


def watch_clipboard(callback):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
    clipboard.connect(SIGNAL_NEW_CLIPBOARD_CONTENT, callback)


def watch_stdin():
    stdin_capture = StdinCapture(os.getpid())
    stdin_capture.start()
    return stdin_capture


class StdinCapture(multiprocessing.Process):

    def __init__(self, parent_pid):
        super(StdinCapture, self).__init__()

        self._parent = parent_pid

        self._input_queue = queues.SimpleQueue()
        self._update_queue = queues.SimpleQueue()

        signal.signal(signal.SIGALRM, self._handle_SIGALRM)
        signal.signal(signal.SIGINT, self._handle_SIGINT)

    def run(self):
        sys.stdin = os.fdopen(0)
        while True:
            logger.debug('Capturing STDIN')
            try:
                value = raw_input()
                logger.debug('Captured "%s" from STDIN', value)
                self._input_queue.put(value)
                os.kill(self._parent, signal.SIGALRM)
            except _UpdateInterrupt as update:
                logger.debug('Updating history with "%s"', update)
                readline.add_history(str(update))
            except EOFError:
                logger.debug('Received an EOF, terminating')
                break

    def update_history(self, update):
        self._update_queue.put(update)
        os.kill(self.pid, signal.SIGALRM)

    def get_input(self):
        return self._input_queue.get()

    def _handle_SIGALRM(self, signal, frame):
        update = self._update_queue.get()
        raise _UpdateInterrupt(update)

    def _handle_SIGINT(self, signal, frame):
        logger.debug('Quitting STDIN capture')
        exit(0)


class _UpdateInterrupt(Exception):
    pass
