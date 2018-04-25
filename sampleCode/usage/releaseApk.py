#coding:utf8

import os
import sys
import platform
import requests
import subprocess
from emailModule import EmailSender

def exeShellCmd(cmd):

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    cmdRetBytes = popen.stdout.read()
    cmdRetStr = str(cmdRetBytes, encoding='utf-8')
    print(cmdRetStr)
    return cmdRetStr

def uploadPgyer():

    # start upload pgyer
    print('start upload pgyer !!!')
    
    url = 'https://www.pgyer.com/apiv2/app/upload'
    
    path = 'android/app/build/outputs/apk/online/release/app-online-release.apk'
    print(path)

    apiEnv = 'QA环境'
    if('online' in sys.argv):
        apiEnv = '生产环境'

    #  params 参考蒲公英上传API
    params = {
        "uKey": (None, "xxx"),
        "_api_key": (None, "xxx"),
        "file":('app-online-release.apk',open(path,'rb'),'application/x-zip-compressed'),
        "buildUpdateDescription": (None, apiEnv)
    }
    
    response = requests.post(url, files=params)
    
    #  deal response
    jsonData = response.json()
    print(jsonData)
    dataObj = jsonData.get('data')
    urlKey =  jsonData.get('data').get('buildShortcutUrl')
    shortcutUrl = 'https://www.pgyer.com/'+urlKey
    appQRCodeURL = jsonData.get('data').get('buildQRCodeURL')
    buildVersion = dataObj.get('buildVersion')
    buildBuildVersion = dataObj.get('buildBuildVersion')
    print('upload pgyer success!!! appShortcutUrl :')
    print(shortcutUrl)
    print(appQRCodeURL)

    gitCmd = 'git log -20 --pretty=format:%h--%s--%an--%cr --no-merges' # 最近20条提交日志
    popen = subprocess.Popen(gitCmd, stdout=subprocess.PIPE, shell=True)
    originStr = popen.stdout.read() # 得到的是bytes字符串
    gitRecentlyCommitMsg = str(originStr, encoding='utf-8')
    print(gitRecentlyCommitMsg)

    formatCommitMsg = gitRecentlyCommitMsg.replace('\n','<br/>')

    if('noemail' in sys.argv):
        print('complete package work, without send a email.')
        return

    print('start send emails !!!')
    email_content = """
        <p>  hi all:</p>
        <p>安卓最新测试包，请点击下面链接查看详情，或扫描二维码直接下载。</p>
        <p> 蒲公英build 版本号：%s</p>
        <p> App 版本：%s, apiEnv : %s </p>
        <p><a href=%s>App详情页</a></p>
        <p> App二维码：</p>
        <p><img src=%s></p>
        <p>最近20条提交日志，<b>格式：简短hash--commitMsg--anthor--time</b></p>
        <p>%s</p>
        """%(buildBuildVersion, buildVersion, apiEnv, shortcutUrl, appQRCodeURL,
             formatCommitMsg)

    sender = EmailSender()
    sender.send(email_content)
    print('complete package work!!!')

def updateGitRepo():
    print('update git repo start')
    ret = exeShellCmd('git pull')
    hasError = 'error' in ret  
    if(hasError):
        raise ValueError('git pull failed')
    ret = exeShellCmd('cd android && git pull')
    hasError = 'error' in ret  
    if(hasError):
        raise ValueError('git pull failed')
    
    print('update git repo end')
    return

def exeGradleCmd():
    print('gradle release apk file all channels ? ', 'all' in sys.argv)
    sysstr = platform.system()
    cmdPrefix = './gradlew'
    if(sysstr =="Windows"):
         print ("Call Windows tasks")
         cmdPrefix = 'gradlew'
    elif(sysstr == "Linux"):
         print ("Call Linux tasks")
    else:
         print ("Other System tasks")

    suffix = '-PhostType=4'
    if('online' in sys.argv):
        suffix = '-PhostType=3' 

    cmdStr = 'cd android && %s clean assembleOnlineReleaseChannels -PchannelList=medlinker %s' %(cmdPrefix, suffix)
    print (cmdStr)
    os.system(cmdStr)
    return


if __name__ == '__main__':

    print (sys.argv)
    updateGitRepo()
    exeGradleCmd()
    uploadPgyer()


