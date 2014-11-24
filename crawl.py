#!/usr/bin/env python
# encoding=utf-8

import Queue
import threading
import time, random
from crawlAPI import CrawlAPI

THREADING_NUM = 5

class Craw(object):

    def __init__(self, n):
        '''
        will download n * categories * subcategories
        now, subcategories is 2, and categories is 27, then total numbers is n * 2 * 27 = n * 54
        @n: download the numbers of app in one subcatorgories
        '''
        self.n = n
        self._api = CrawlAPI()
        self._q = Queue.Queue()
        self._endProcess = False

    def crawlAppInfo(self):
        print 'start crawl app info ...'
        subcategory = ['apps_topselling_free', 'apps_topselling_new_free']
        categories = self._api.getCategories()
        for title, TAG in categories.iteritems():
            #print TAG
            for item in subcategory:
                print '----------------------------------------------'
                print 'update [%s] [%s]'%(TAG, item)
                print '----------------------------------------------'
                res = self._api.getApps(TAG, item, self.n)
                if res != {}:
                    for title, packageName in res.iteritems():
                        self._q.put((title, packageName))
                    time.sleep(random.randint(1, 5))
        print 'crawl info end ...'

    def downloadApp(self, i):
        while (not self._endProcess) or (not self._q.empty()):
            (appName, packageName) = self._q.get()
            print '----------------------------------------------'
            print 'download [%s] [%s]'%(appName, packageName)
            print '----------------------------------------------'
            self._api.download(packageName)
            if self._q.empty():
                time.sleep(5)
        print 'threading [%s] end ...'%i

    def start(self):
        '''
        start to crawl and download
        '''
        threads = []
        for i in range(THREADING_NUM):
            print 'create download threading ... %s'%i
            thread = threading.Thread(target=self.downloadApp, args=(i,))
            thread.start()
            threads.append(thread)
        self.crawlAppInfo()
        self._endProcess = True
        for thread in threads:
            if thread.is_alive:
                thread.join()

if __name__ == '__main__':
    print 'start...'
    app = Craw(20)
    app.start()
    print 'end..'
