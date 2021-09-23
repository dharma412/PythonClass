import time
import common.gui.guiexceptions as guiexceptions

class Wait():
    """ Waiting for events to happen """

    def __init__(self, until=None, msg=None, timeout=60, interval=1,
        raise_exception=True):
        """Specifies the until condition we'll check, the message we'll use  when we fail, a timeout, and an interval.
        If raise_exception is not True, False is returned instead of raising Exception
        'until' is a function that return True or False. Functions will all arguments can be passed using lambda.
        Example: Wait(until=lambda: my_func(arg1, arg2)) """

        self.timeout = timeout
        self.interval = interval
        self.until = until
        self.msg = msg or "Waited for %s seconds with interval %s." % \
                (self.timeout, self.interval)
        self.raise_exception = raise_exception

    def wait(self, *args, **kwargs):
        """Wait until the "until" condition returns true or the timeout happens.Arguments are passed to until function.
        """
        if self.until is None:
            raise Exception('Until condition is not specified.')
        for i in xrange(0, self.timeout, self.interval):
            if self.until(*args, **kwargs):
                # until() returns True we got what we wait for
                return True
            time.sleep(self.interval)
        # expected condition has not been met
        if self.raise_exception:
            raise guiexceptions.TimeoutError(self.msg)
        else:
            return False
