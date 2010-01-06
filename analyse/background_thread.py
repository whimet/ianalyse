import threading
import thread, time
from threading import Lock
from datetime import datetime
import logging

class BackGroundThread:
    _RUNNING = False
    
    def __init__(self, method, interval):
        self.method = method
        self.interval = interval

    def method_wrapper(self):
        logger = logging.getLogger('ianalyse_logger')
        while(True):
            try:
                logger.info("[" + str(datetime.now()) + '] the background thread is processing.')
                self.method()
                logger.info("[" + str(datetime.now()) + '] the background thread go sleep..')
            except Exception, e:
                logger.error(e)
                pass
            time.sleep(self.interval)

    def launch(self):
        lock = Lock()
        lock.acquire()
        if BackGroundThread._RUNNING :
            return False
        BackGroundThread._RUNNING = True
        lock.release()
        t = threading.Thread(target=self.method_wrapper)
        t.setDaemon(True)
        t.start()
        return True        

        
