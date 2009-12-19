import threading
import thread, time
from datetime import datetime

class BackGroundThread:
    _RUNNING = False
    
    def __init__(self, method, interval):
        self.method = method
        self.interval = interval

    def method_wrapper(self):
        while(True):
            try:
                print "[" + str(datetime.now()) + '] the backgrond thread is processing.'
                self.method()
                print "[" + str(datetime.now()) + '] the backgrond thread go sleep..'
            except Exception, e:
                print e
                pass
            time.sleep(self.interval)

    def launch(self):
        if BackGroundThread._RUNNING :
            return False

        BackGroundThread._RUNNING = True
        t = threading.Thread(target=self.method_wrapper)
        t.setDaemon(True)
        t.start()
        return True
