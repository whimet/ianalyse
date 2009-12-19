import threading
import thread, time

class BackGroundThread:
    def __init__(self, method):
        self.method = method

    def method_wrapper(self):
        while(True):
            time.sleep(15)
            try:
                print 'background process is lauched...'
                self.method()
            except Exception, e:
                print e
                pass


    def launch(self):
        t = threading.Thread(target=self.method_wrapper)
        t.setDaemon(True)
        t.start()
        return True
