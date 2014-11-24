#!/usr/bin/env python
# coding=utf-8

import os
import time
import random
from googleplay_api import config
from googleplay_api.googleplay import GooglePlayAPI
from googleplay_api.helpers import sizeof_fmt, print_header_line, print_result_line

class CrawlAPI:
    '''
    craw interface
    '''
    def __init__(self):
        self._android_id = config.ANDROID_ID
        self._user = config.GOOGLE_LOGIN
        self._passwd = config.GOOGLE_PASSWORD
        self._auth_token = config.AUTH_TOKEN
        self._savePath = config.SAVE_PATH
        self._api = self._login()

    def _configTest(self):
        if any([each == None for each in [self._android_id, self._user, self._passwd]]):
            raise Exception('config item for login is not correct...')
        if self._savePath[-1] != '/':
            self._savePath += '/'

    def _login(self):
        '''
        user android_id, user name and password or AUTH_TOKEN to login
        '''
        self._configTest()
        api = GooglePlayAPI(self._android_id)
        api.login(self._user, self._passwd, self._auth_token)
        return api

    def getCategories(self):
        '''
        get categories from googleplay
        @return: {'category_name','url_params'}
        '''
        res = self._api.browse()
        if res == False:
            return False
        category_dict = {}
        for c in res.category:
            category_dict[c.name] = c.dataUrl[c.dataUrl.rfind('=')+1:]
        return category_dict

    def getApps(self, category, subCategory, nb_result=20, offset=20):
        '''
        get apps from a subcategory in categories
        '''
        apps = {}
        res = self._api.list(category, subCategory, str(offset), 0)
        doc = res.doc[0]
        nextPageUrl =  doc.containerMetadata.nextPageUrl
        #print nextPageUrl
        for c in doc.child:
            #print c.title, c.details.appDetails.packageName
            apps[c.details.appDetails.packageName] = c.title
        stop = False
        i = 0
        i += int(offset)
        time.sleep(random.randint(1, 5))
        print 'wait...have get: %s'%i
        while (not stop):
            res = self._api.getNextPage(nextPageUrl)
            if res == False:
                print 'no more app'
                break 
            doc = res.doc[0]
            nextPageUrl =  doc.containerMetadata.nextPageUrl
            #print nextPageUrl
            for c in doc.child:
                #print c.title, c.details.appDetails.packageName
                apps[c.details.appDetails.packageName] = c.title
            i += int(offset)
            time.sleep(random.randint(1, 5))
            print 'wait...'
            if i > nb_result:
                stop = True
        return apps

    def search(self, name, offset=None, num=None):
        '''
        search app
        @name: app name
        @offset: start position
        @num: app num
        @return: search result
        '''
        try:
            message = self._api.search(name, num, offset)
        except Exception as e:
            print e
            return False
        if message == False:
            return False
        return message

    def getDetails(self, packageName):
        message = self._api.details(packageName)
        #print message
        if message == False:
            return '', '', ''
        doc = message.docV2
        #versionString = doc.details.appDetails.versionString
        version = doc.details.appDetails.versionCode
        offerType = doc.offer[0].offerType
        size = sizeof_fmt(doc.details.appDetails.installationSize)
        return version, offerType, size

    def download(self, packageName):
        vc, ot, sz = self.getDetails(packageName)
        if vc == '' or ot == '':
            print 'can\'t get details info ...'
            return False
        saveName = packageName + '_' + str(vc)
        if saveName not in os.listdir(self._savePath):
            print 'start download ... size: %s'%sz
            data = self._api.download(packageName, vc, ot)
            open(self._savePath + saveName, 'wb').write(data)
            print 'complated ...'
        else:
            print 'replicate app ... next one ...'


if __name__ == '__main__':
    app = CrawlAPI()
    #res =app.search('angrybird', '1', '1')
    #res = app.getCategories()
    #print res
    #app.getApps('GAME', 'apps_topselling_free', '300', '20')
    #app.getDetails('com.facebook.katana')
    app.download('com.facebook.katana')