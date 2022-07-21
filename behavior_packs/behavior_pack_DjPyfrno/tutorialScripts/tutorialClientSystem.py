# -*- coding: utf-8 -*-

# 获取客户端引擎API模块
import mod.client.extraClientApi as clientApi
# 获取客户端system的基类ClientSystem
ClientSystem = clientApi.GetClientSystemCls()

# 在modMain中注册的Client System类
class TutorialClientSystem(ClientSystem):

    # 客户端System的初始化函数
    def __init__(self, namespace, systemName):
        # 首先初始化TutorialClientSystem的基类ClientSystem
        super(TutorialClientSystem, self).__init__(namespace, systemName)
        print "==== TutorialClientSystem Init ===="
        # 注册自定义的page
        # 先import定义好的页面类
        from tutorialScripts.pages.myNoTitlePage import MyNoTitlePage
        from tutorialScripts.pages.myTitlePage import MyTitlePage
        from tutorialScripts.pages.customCompPage import MyCustomCompPage
        from tutorialScripts.pages.buttonPage import MyButtonPage
        from tutorialScripts.pages.addrPage import MyAddrPage
        from tutorialScripts.pages.recyclePage import MyRecyclePage
        # 获取书本管理对象，详细用法见“05-常见脚本对象”
        bookManager = clientApi.GetBookManager()
        # 注册自定义的页面类，同时为它们命名，这些名称是在json中使用的
        bookManager.AddPageType("CustomMod:MyNoTitlePage", MyNoTitlePage)
        bookManager.AddPageType("CustomMod:MyTitlePage", MyTitlePage)
        bookManager.AddPageType("CustomMod:MyCustomCompPage", MyCustomCompPage)
        bookManager.AddPageType("CustomMod:MyButtonPage", MyButtonPage)
        bookManager.AddPageType("CustomMod:MyAddrPage", MyAddrPage)
        bookManager.AddPageType("CustomMod:MyRecyclePage", MyRecyclePage)
        print "============== add MyTestPage success =============="
 

    # 函数名为Destroy才会被调用，在这个System被引擎回收的时候会调这个函数来销毁一些内容
    def Destroy(self):   
        pass
