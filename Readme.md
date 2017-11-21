# iOS 原生内嵌 RN, python 脚本实现
## 概述
网上很多教程中, `iOS` 原生内嵌 `RN` 也是有许多方法的,但是许多方法繁琐易错.
尤其是手动桥接 `RN`的工程, `'BatchedBridge', # 0.45` 版本以后需要添加,否则会报错.

`iOS` 原生包 `RN`, 即为以`iOS`为基础工程,在指定的页面,包入`react native`提供的`RCTRootView`页面.
因过程较为繁琐,涉及`podfile`生成,初始化`RN`工程,指定版本,启动 `RN`本地服务器等等,不一而足, 因此采用 `Python`调用系统的`shell`脚本来完成.
[参考文章 -- reactnative集成到原生ios项目](https://www.tuicool.com/articles/BfInEv)

## 前提
* 已经安装并配置好了`React native`环境
* 已经安装并配置好了`CocoaPods`环境
* 使用 `Mac OSX`, 自带`Python 2.x`环境
* 我们不使用参考链接中的手动拖曳的方式添加`RN`工程,而是采用`CocoaPods`的本地映射方式管理`RN`

## 使用
* 新建一个原生的`iOS`工程, 假设名为 `ApplePrj`
* 将本文件拷贝至`ApplePrj`同目录下
* 在终端中 `cd`到`ApplePrj`锁在目录, 然后执行`python rnPrjInit`即可
* 如果中间没有问题,会执行到本地服务器启动的页面

## 下面是执行过程 --- 旨在记录脚本究竟做了什么
以下为同步执行的过程

* 根据`.py`文件中设定好的`RN`版本,在原生工程的同级目录下,去生成一个名为`ReactNativePrj`的`RN`原生工程.
  > PS: 此时工程生成的两个包含各自平台的文件夹,`ios`和`android`文件夹,其实是没有用的,可以删掉.不删掉也没事.
* 获取`ApplePrj`锁在目录的文件夹名称, 即假设文件目录为`~/user/bin/ApplePrj`,我需要获取工程的名称,也就是这里的目录文件名`ApplePrj`,也就是`iOS`原生工程的文件名.
* 根据设置好的`ios`版本,在当前目录下,去生成一个`Podfile` --- 这里可以省去编写`dependency`的麻烦,不过如果有新的依赖库,可以在生成后自行修改,然后再单独执行`pod update`命令
* 执行`Podfile`中的指令,相当于在终端中执行`pod update`. -- 此时里面的 `target PrjName do`,`PrjName`已经在上面获取到了工程的名称.
* 执行成功后,`cd`到`RN`的工程中,执行`react-native start`开启本地服务器.
* 此时有可能会失败,需要进一步执行`chmod -R 777 node_modules`


## 内嵌成功后
如果是初次初始化的 `Xcode` 工程,要记得开启网络权限.
其次就是添加入 `RN` 的 `View`
下面是部分代码

```objc

#import <React/RCTBundleURLProvider.h>
#import <React/RCTRootView.h>

//...中间省略部分
- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    NSURL *jsCodeLocation;
    jsCodeLocation = [[RCTBundleURLProvider sharedSettings] jsBundleURLForBundleRoot:@"index.ios" fallbackResource:nil];
    
    RCTRootView *rootView = [[RCTRootView alloc] initWithBundleURL:jsCodeLocation
                                                        moduleName:@"ReactNativePrj"
                                                 initialProperties:nil
                                                     launchOptions:nil];
    rootView.frame = self.view.frame;
    UIViewController *vc = [[UIViewController alloc] init];
    vc.view.backgroundColor = [UIColor redColor];
    [vc.view addSubview:rootView];
    
    [self.navigationController pushViewController:vc animated:YES];
}
```

* `index.ios` 是对应的 JS 代码
* `ReactNativePrj`是上面那段 JS 代码中注册的 JS 组件名称.
> `AppRegistry.registerComponent('ReactNativePrj', () => ReactNativePrj);`

* 引入的 `RCRootView`顾名思义, 就是 `RN` 对应的视图,所有的视图信息都是在这个容器中变化.

以上,谢谢.





