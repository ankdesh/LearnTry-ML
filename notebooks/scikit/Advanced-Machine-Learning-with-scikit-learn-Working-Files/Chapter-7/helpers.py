import time

class Timer(object):
    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        elapsed = (time.time() - self.tstart)
        mins, secs = divmod(elapsed, 60)
        elapsed_string = "Elapsed: "
        if mins > 0:
            elapsed_string += "%dm " % mins
        elapsed_string += "%ds" % secs
        
        print(elapsed_string)