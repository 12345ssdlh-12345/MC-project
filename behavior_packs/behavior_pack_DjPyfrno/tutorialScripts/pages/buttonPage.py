#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取预设页面类 TitlePage
TitlePage = bookManager.GetTitlePageCls()
# 获取预设组件类 ButtonComp
ButtonComp = bookManager.GetButtonCompCls()

class MyButtonPage(TitlePage):
    """
        本例子实现了两个Button的用法：1. 点击提示消息 2. 点击跳转页面
    """
    def __init__(self, size = None, position = None):
        # 调用父类同名方法，TitlePage 会自动添加标题组件以及提供标题组件注入数据的方法，排版的方法。
        TitlePage.__init__(self, size, position)  
        self.button1 = ButtonComp()    
        self.button2 = ButtonComp()    
        self.AddComps(self.button1, self.button2)

    def SetData(self, data):
        # TitlePage 会调用 self.data 从中获取json数据。
        self.data = data
        return self

    def ShowMsg(self, msg):
        # 获取button1组件所封装的UI控件根节点
        buttonNode = self.button1.GetRootUINode()
        # 使用GetNodeCenterGlobal获取该根节点中心的全局坐标
        position = self.button1.GetNodeCenterGlobal(buttonNode)
        # 显示提示消息
        bookManager.ShowMsg(position, msg)

    def GoToPage(self, entryIdentifier, pageNum):
        # 获取特定章节对象，这里的用法请参考文档中 "常用脚本对象" 章节
        entry = bookManager.GetOpeningBookInstance().GetEntry(entryIdentifier)
        # 跳转到该章节的某一页（从第0页开始算）
        bookManager.To(entry.GetAddr() + "/{0}".format(pageNum))

    def Show(self):
        if self.data:
            # 注入数据，先给标题注入数据
            self.SetTitleData()
            # 给Button注入数据和函数回调

            showMsgCallback = {
                "func": self.ShowMsg,
                "args": [self.data.get("clickMsg", "点击了苹果")]
            }

            toPageCallback = {
                "func": self.GoToPage,
                "args": [self.data.get("jumpEntry", "highlightEntry"), self.data.get("pageNum", 0)]    # 跳转到"highlightpage"这一章节的第2页（从0页开始算）
            }

            self.button1.SetDataBeforeShow(defaultImage="textures/items/apple", pressCallBack=showMsgCallback)
            self.button2.SetDataBeforeShow(defaultImage="textures/items/bucket_milk", pressCallBack=toPageCallback)
            
            # 执行基础类的方法获取节点并显示出来
            TitlePage.Show(self)
            # 排版位置，先重置所有组件相对页面的位置，保证每次调用Show的时候组件的Move都是相对于Page的原点
            self.ResetCompsPosition()   
            pageCenter = self.Center()    
            pageSize = self.GetSize() 
            
            # 排版标题并获取内容开始的坐标y值
            content_begin = self.LayoutTitle()
            
            # 布局自己的组件，组件在调用Align以及Move方法前需要先调用SetSize方法，因为这些方法都是基于GetSize来计算的。
            # 对 button1 设置大小后，将其中心对齐到页面的中心，将其上边界与 标题 的下边界对齐，然后往下移动5px
            self.button1.SetSize((40, 40)).AlignCenterToX(pageCenter[0]).AlignTopToY(content_begin).MoveY(5)
            # 对 button2 设置大小后，将其中心对齐到页面的中心，将其上边界与 button1 的下边界对齐，然后往下移动10px
            self.button2.SetSize((40, 40)).AlignCenterToX(pageCenter[0]).AlignTopToY(self.button1.Bottom()).MoveY(10)
            return self
        else:
            print "in MyButtonPage Show: no data present"
            return self
        



        
