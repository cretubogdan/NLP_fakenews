from Logger import *
from queue import Queue
from threading import Thread, Event
import multiprocessing

class Worker(Thread):

    def __init__(self, name, queue, results, abort, idle):
        Thread.__init__(self)
        self.logger = Logger()
        self.name = name
        self.queue = queue
        self.results = results
        self.abort = abort
        self.idle = idle
        
        self.logger.Log(Severity.INFO, "Worker [{0}] initialization succesfully".format(self.name))

        self.start()


    def run(self):
        self.logger.Log(Severity.INFO, "Worker [{0}] started".format(self.name))
        while not self.abort.is_set():
            try:
                func, args, kwargs = self.queue.get(False)
                self.logger.Log(Severity.INFO, "Worker [{0}] got a new job to do".format(self.name))
                self.idle.clear()
            except:
                self.idle.set()
                continue

            try:
                self.logger.Log(Severity.INFO, "Worker [{0}] started job {1}".format(self.name, func.__name__))
                result = func(*args, **kwargs)
                if result is not None:
                    self.results.put(result)
                    self.logger.Log(Severity.INFO, "Worker [{0}] finished job".format(self.name))
            except:
                self.logger.Log(Severity.ERROR, "Worker [{0}] couldn't finish job {1}".format(self.name, func.__name__))
            finally:
                self.queue.task_done()


class WorkPool:

    INTERVAL_CHECK_ALIVE = 1

    def __init__(self):
        self.logger = Logger()
        self.thread_count = 2 * multiprocessing.cpu_count() - 1
        self.queue = Queue(0)
        self.results_queue = Queue(0)

        self.aborts = []
        self.idles = []
        self.threads = []

        self.logger.Log(Severity.INFO, "WorkPool initialization succesfully with # of cores {0}".format(self.thread_count))

    def __del__(self):
        self.logger.Log(Severity.INFO, "WorkPool starts aborting for {0} workers".format(self.thread_count))
        self.abort()

    def abort(self):
        for a in self.aborts:
            self.logger.Log(Severity.INFO, "WorkPool made a new abort")
            a.set()

    def run(self):
        if self.alive():
            self.logger.Log(Severity.INFO, "WorkPool already running")
            return False

        self.logger.Log(Severity.INFO, "WorkPool will be started with # of cores {0}".format(self.thread_count))

        for n in range(self.thread_count):
            abort = Event()
            idle = Event()
            self.aborts.append(abort)
            self.idles.append(idle)
            self.threads.append(Worker("#id-{0}".format(n), self.queue, self.results_queue, abort, idle))

        self.logger.Log(Severity.INFO, "WorkPool started running");
        return True


    def get_results(self):
        results = []
        while not self.idle():
            continue
        try:
            while True:
                results.append(self.results_queue.get(False))
                self.results_queue.task_done()
        except:
            pass

        return results


    def alive(self):
        return True in [t.is_alive() for t in self.threads]

    def idle(self):
        return False not in [i.is_set() for i in self.idles]

    def done(self):
        return self.queue.empty()

    def enqueue(self, func, *args, **kwargs):
        self.logger.Log(Severity.INFO, "New job [{0}] added to the WorkPool".format(func.__name__))
        self.queue.put((func, args, kwargs))
