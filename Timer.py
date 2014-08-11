'''
 There are two classes in this file and both are threads

 1. TickGenerator
 2. TickFetcher
'''

import sys
import time
import threading
import traceback
import Queue
from collections import namedtuple

# Thread duration
#THREAD_SLEEP        = .1
THREAD_SLEEP       = .001 # For testing

# Message format
Message = namedtuple("message", "type value1 value2")

# Message types
MSG_TYPE_TIME       = 0
MSG_TYPE_PHASE      = 1

# Phases (for one pomodori)
'''
    Phase1: work
    Phase2: break
    Phase3: work
    Phase4: break
    ...
    Phase8: long_break
'''
PHASE_WORK          = "w" # This string value means nothing. Only for the dictionary.
PHASE_BREAK         = "b" # Same
PHASE_LONGBREAK     = "l" # Same
PHASE_FINISHED      = "f" # duh.
PHASES = {PHASE_WORK: 25, PHASE_BREAK: 5, PHASE_LONGBREAK: 15}


# Generates tick events and put it into the message queue
class TickGenerator(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        # Defines the thread is running or paused (Event.set() or Event.clear())
        self._running = threading.Event()
        # Let's try simple bool type variable instead of threading.Event() object.
        # But it's not wrong but also NOT really safe!
        self._finished = False

    def run(self):
        try:
            self._run_proc()
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            # TODO: log module should be employed
            file_name, line_num, func_name, code = traceback.extract_tb(exc_tb)[-1]
            print 'Exception %s: %s in %s' % \
                (exc_type.__name__, exc_value, threading.current_thread().name)
            print 'Caused by: %s, %s (%s), %s' % \
                (file_name, func_name, line_num, code)

    def _run_proc(self):
        for current_phase in range(1, 9):
            mins = 0

            # Odd numbers: work
            # Even numbers: break or long break
            if current_phase % 2 != 0:
                mins = PHASES[PHASE_WORK]
            else:
                if current_phase == 8: # Last phase
                    mins = PHASES[PHASE_LONGBREAK]
                else:
                    mins = PHASES[PHASE_BREAK]

            secs = mins * 60
            # Below line is possible only because each key-value combination is unique.
            self.sendMessage(MSG_TYPE_PHASE, PHASES.keys()[PHASES.values().index(mins)], current_phase)
            self._running.set()

            '''
            [NOTE]
            1. secs * 10
                Since this loop iterates 10 times per second due to "sleep() 100ms",
                the range must be 10 times bigger than intended seconds.
            2. +9
                Decreasing seconds should starts from 900ms
                For example, ticking from 2s to 1s.
                2.0s -> 1.9s (wrong. it will print out 2 -> 1 within 0.1sec)
                2.9s -> 2.8s (right. still "2" and 2.9 -> 2.0 takes 1sec)
            '''
            for tick in range((secs * 10) + 9, -1, -1):
                if self._finished:
                    break
                self._running.wait()
                self.now = tick / 10
                self.sendMessage(MSG_TYPE_TIME, self.now)
                time.sleep(THREAD_SLEEP)
            if self._finished:
                break
        self.sendMessage(MSG_TYPE_PHASE, PHASE_FINISHED, 0);

    def sendMessage(self, type, value1, value2=None):
        msg = Message(type, value1, value2)
        self.queue.put(msg)

    def pause(self, set_pause):
        if set_pause:
            self._running.clear()
        else:
            self._running.set()

    def isPaused(self):
        return not self._running.isSet()

    def finish(self):
        self._finished = True
        if self.isPaused():
            self.pause(False)
        self.join()

    def isFinished(self):
        return self._finished


# Fetches tick messages from the message queue
# "func" should be implemented for the message processing
class TickFetcher(threading.Thread):
    def __init__(self, func, queue):
        threading.Thread.__init__(self)
        self.func = func
        self.queue = queue
        self._finished = False

    def run(self):
        try:
            self._run_proc()
        except:
            exc_type, exc_value, exc_tb = sys.exc_info()
            file_name, line_num, func_name, code = traceback.extract_tb(exc_tb)[-1]
            print 'Exception %s: %s in %s' % \
                (exc_type.__name__, exc_value, threading.current_thread().name)
            print 'Caused by: %s, %s (%s), %s' % \
                (file_name, func_name, line_num, code)

    def _run_proc(self):
        while not self._finished:
            if not self.queue.empty():
                msg = self.queue.get(0)
                self.func(msg)
            time.sleep(THREAD_SLEEP)

    def finish(self):
        self._finished = True
        self.join(1)
