#coding:utf8

import os
import sys
import platform
import requests


# 上传蒲公英栗子
def uploadPgyer():

    # start upload pgyer
    print('start upload pgyer !!!')
    
    url = 'https://qiniu-storage.pgyer.com/apiv1/app/upload'
    
    path = 'android/app/build/outputs/apk/online/release/app-online-release.apk'
    print(path)
    
    #  params
    params = {
        "uKey": (None, "xxx-ukey"),
        "_api_key": (None, "xxx-api-key"),
        "file":('app-online-release.apk',open(path,'rb'),'application/x-zip-compressed')
    }
    
    response = requests.post(url, files=params)
    
    #  deal response
    jsonData = response.json()
    print(jsonData)
    urlKey =  jsonData.get('data').get('appShortcutUrl')
    shortcutUrl = 'https://www.pgyer.com/'+urlKey
    appQRCodeURL = jsonData.get('data').get('appQRCodeURL')
    print('upload pgyer success!!! appShortcutUrl :')
    print('https://www.pgyer.com/%s'% urlKey)
    print(shortcutUrl)
    print(appQRCodeURL)

    print('complete package work!!!')
    
    return 



