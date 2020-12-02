import sys
import threading
import time


MUTEX = '__mutex__'


class A:

    def __init__(self):
        self.contents = {MUTEX: None}

    def add_to_list(self, key, value):
        # Because of the GIL, a key in the dictionary can be treated like a mutex if we delete it
        # and put it back when we're done.
        contents = self.contents

        while True:
            try:
                del contents[MUTEX]
                break
            except KeyError:
                time.sleep(0.001)
                continue

        if key not in self.contents:
            contents[key] = [value]
        else:
            contents[key].append(value)

        contents[MUTEX] = None


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
