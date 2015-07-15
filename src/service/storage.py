import time

import toro
import tornado.ioloop
import tornado.gen
import tornado.web


class Client():
    def __init__(self):
        self.queued_items = toro.Queue()

    @tornado.gen.coroutine
    def watch_queue(self):
        while True:
            items = yield self.queued_items.get()
            ''' download file and storage index  '''
            # go_do_some_thing_with_items(items)


'''
    ###################
    from tornado import queues
    from tornado import gen
        q = queues.Queue(maxsize=2)
        q.put(100)
        q.put(2000)
    q = queues.Queue(maxsize=2)


    @gen.coroutine
    def consumer():
        while True:
            item = yield q.get()
            try:
                print('Doing work on %s' % item)
                yield gen.sleep(0.01)
            finally:
                q.task_done()

    @gen.coroutine
    def producer():
        for item in range(5):
            yield q.put(item)
            print('Put %s' % item)


    @gen.coroutine
    def the_queue():
        consumer()           # Start consumer.
        yield producer()     # Wait for producer to put all tasks.
        # yield q.join()       # Wait for consumer to finish all tasks.
        # print('Done')

    tornado.ioloop.IOLoop().run_sync(the_queue)

    # from src.service.storage import Client
    # client = Client()
    # tornado.ioloop.IOLoop.instance.add_callback(client.watch_queue)
    ###################
'''