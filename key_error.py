import sys
import threading
import time


class A:

    def __init__(self):
        self.contents = {i: None for i in range(100)}

    def add_to_list(self, key, value):
        contents = self.contents

        while True:
            try:
                # Because of the GIL, a key in the dictionary can be treated like a mutex if we
                # delete it and put it back when we're done. This works because only one thread
                # will hold the GIL and be able to delete the mutex, all the others will block in
                # the sleep loop until the thread puts it back
                values = contents.pop(key)
            except KeyError:
                time.sleep(0.001)
                continue

            if values is None:
                values = []
            values.append(value)
            contents[key] = values
            break


class T(threading.Thread):

    def __init__(self, a):
        self.a = a
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        time.sleep(0.001)
        for j in range(10):
            for i in range(100):
                a.add_to_list(i, j)


a = A()
threads = []
for t in range(100):
    thread = T(a)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

for i in range(100):
    try:
        assert len(a.contents[i]) == 10 * 100
    except AssertionError:
        print("FAILED", i, len(a.contents[i]))
        sys.exit(1)
