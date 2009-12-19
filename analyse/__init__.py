from analyse.background_thread import BackGroundThread
from analyse.cache import Cache
from analyse.config import Configs

bgt = BackGroundThread(Cache.INSTANCE().populate, 600)
bgt.launch()