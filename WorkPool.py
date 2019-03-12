from Logger import *
from threading import Thread, Lock
import queue
import multiprocessing


class IWorker(Thread):
    def run(self):
       pass 


class WorkPool:
    num_workers = None
    q = None
    lock_singleton = Lock()
    lock_task = Lock()
    logger = Logger()
    
    def __init__(self):
        WorkPool.lock_singleton.acquire()
        WorkPool.num_workers = max(1, multiprocessing.cpu_count() * 2 - 1)
        
        if None == WorkPool.q:
            WorkPool.q = queue.Queue()
            WorkPool.counter_active_workers = 0
            WorkPool.logger.Log(Severity.INFO, "Work pool initialization completly")
            WorkPool.logger.Log(Severity.INFO, "Work pool with {0} workers".format(WorkPool.num_workers))

        WorkPool.lock_singleton.release()

    def AddTask(self, task):
        WorkPool.q.put(task)

    def GetTask():
        to_return = None
        WorkPool.lock_task.acquire()
        while WorkPool.q.empty():
            continue
        to_return = WorkPool.q.get()
        WorkPool.lock_task.release()
        return to_return

    def Start(self):
        workers = []
        for t in range(WorkPool.num_workers):
            worker = self.GetTask()
            workers.append(worker)
        for t in range(WorkPool.num_workers):
            workers[t].start()
        for t in range(WorkPool.num_workers):
            workers[t].join()


