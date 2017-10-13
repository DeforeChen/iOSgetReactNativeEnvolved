#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

## 获取工程名称
def fetchPrjName():
        # 从当前文件路径获取到锁在文件夹名称,作为路径名
    os.chdir('./')
    curPath = os.getcwd()
    prjName = os.path.basename(curPath)
    print(prjName)
    return prjName


'''
platform:ios, '8.0'
# use_frameworks!
# 添加本地 RN 依赖
pod 'React', :path => './ReactNativePrj/node_modules/react-native', :subspecs => [
    'Core',
    'ART',
    'RCTActionSheet',
    'RCTAdSupport',
    'RCTGeolocation',
    'RCTImage',
    'RCTNetwork',
    'RCTPushNotification',
    'RCTSettings',
    'RCTText',
    'RCTWebSocket',
    'RCTLinkingIOS',
    'BatchedBridge',
]

pod "Yoga", :path => "./ReactNativePrj/node_modules/react-native/ReactCommon/yoga"

target 'GetRNEnvolved' do
end
    
'''

## 生成 podffile 文件
def fetchPodfileContent(iosVersion,prjName):
    title = "platform:ios, '"+ iosVersion +"'" +"\n# use_frameworks!\n# 添加本地 RN 依赖\n"
    path = '''pod 'React', :path => './ReactNativePrj/node_modules/react-native', :subspecs => [\n'''
    content = '''\
    'Core',\n\
    'ART',\n\
    'RCTActionSheet',\n\
    'RCTAdSupport',\n\
    'RCTGeolocation',\n\
    'RCTImage',\n\
    'RCTNetwork',\n\
    'RCTPushNotification',\n\
    'RCTSettings',\n\
    'RCTText',\n\
    'RCTWebSocket',\n\
    'RCTLinkingIOS',\n\
    'BatchedBridge',\n\
]

pod "Yoga", :path => "./ReactNativePrj/node_modules/react-native/ReactCommon/yoga"\n
'''

    targetContent = "target '" + prjName + '''' do\n\
end
    '''

    return title+path+content+targetContent

def generatePodfile(iosVersion):
    filehandle = open('Podfile', "a")
    filehandle.write(fetchPodfileContent(iosVersion,fetchPrjName()))
    filehandle.close()

## 根据版本号,生成初始化 RN 工程的命令
def fetchRN_InitCmd(rnVersion):
    initRN = 'rninit init '+ 'ReactNativePrj' +' --source react-native@' + rnVersion
    return initRN

def main():
    rnInitCmd = fetchRN_InitCmd('0.47.0')
    if os.system(rnInitCmd) == 0: #表示初始化完毕,开始生成对应的pod 文件
        generatePodfile('8.0')
        res = os.system('pod install')
        if res == 0:
            print('========== Podfile 安装完毕,开始启动本地服务器! =============================')
            os.chdir('./ReactNativePrj')
            bootLocalService = os.system('react-native start') # 启动本地服务器
            while bootLocalService != 0:
                os.system('chmod -R 777 node_modules')
                bootLocalService = os.system('react-native start') # 启动本地服务器
        else:
            print('========== 请检查当前 podfile 后重试! ========')
    else:
        userWilling = raw_input('==========================================\n生成 RN 工程失败,是否重试? y/n: \n')
        if userWilling == 'y':
            os.system(rnInitCmd)
        else:
            os.system('exit')

        
    

if __name__ == '__main__':
    main()