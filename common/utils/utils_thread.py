# coding=UTF-8

import threading


class NewThread(threading.Thread):

    def __init__(self, func, *args, **kwargs):
        if not callable(func):
            raise Exception('%s is not callable' % func)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        threading.Thread.__init__(self)

    def run(self):
        self.func(*self.args, **self.kwargs)


class ThreadLock():

    def __init__(self):
        self._lock = None

    def acquire_lock(self):
        """
        Acquire the module-level lock for serializing access to shared data.
        This should be released with _releaseLock().
        """
        if (not self._lock):
            self._lock = threading.RLock()
        if self._lock:
            self._lock.acquire()

    def release_lock(self):
        """
        Release the module-level lock acquired by calling _acquireLock().
        """
        if self._lock:
            self._lock.release()
