# -*- coding: UTF-8 -*-

debug = False
if debug:
    import sys, xbmc
    if sys.version_info[0] == 2:
        from xbmc import LOGNOTICE as LOGINFO
    else:
        from xbmc import LOGINFO

import threading
class Thread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self)
        self._target = target
        self._args = args
    def run(self):
        if debug: xbmc.log('start %s ' % self.name, LOGINFO)
        self._target(*self._args)
        if debug: xbmc.log('ende %s ' % self.name, LOGINFO)
