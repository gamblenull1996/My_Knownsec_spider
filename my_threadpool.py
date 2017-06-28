# -*- coding:utf-8 -*-
import logging
from Queue import Queue
from threading import Thread

log = logging.getLogger('spider.threadpool')


class MyThreadPool(object):
    def __init__(self, num_threads=10):
        self.tasks = Queue()
        for i in xrange(1, num_threads + 1):
            log.info('Initialize thread %d' % i)
            MyThread(self.tasks)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))
        log.debug('Add task')

    def get_size(self):
        return self.tasks.qsize()

    def wait_completion(self):
        self.tasks.join()
        log.info('All tasks are done')


class MyThread(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
        log.debug('Thread started...')

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                log.warning('Thread is working...')
                func(*args, **kwargs)
            except Exception as e:
                log.error(e, exc_info=True)
            self.tasks.task_done()
