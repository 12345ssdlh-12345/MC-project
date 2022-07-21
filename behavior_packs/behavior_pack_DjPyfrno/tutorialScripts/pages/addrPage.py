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
# 获取预设组件类 TextComp
TextComp = bookManager.GetTextCompCls()

class MyAddrPage(TitlePage):
    """
        本例子实现了两个Button的用法：1. 点击提示消息 2. 点击跳转页面
    """
    def __init__(self, size = None, position = None):
        # 调用父类同名方法，TitlePage 会自动添加标题组件以及提供标题组件注入数据的方法，排版的方法。
        TitlePage.__init__(self, size, position)  
        self.button1 = ButtonComp()    
        self.button2 = ButtonComp()   
        self.text1 = TextComp(bcf.TextAlign.Fit_Center) 
        self.text2 = TextComp(bcf.TextAlign.Fit_Center) 
        self.AddComps(self.button1, self.button2, self.text1, self.text2)

    def SetData(self, data):
        # TitlePage 会调用 self.data 从中获取json数据。
        self.data = data
        return self

    def GoToPage(self, addr):
        # 跳转到对应地址
        bookManager.To(addr)

    def Show(self):
        if self.data:
            # 注入数据，先给标题注入数据
            self.SetTitleData()
            # 给Button注入数据和函数回调
            toPageCallback1 = {
                "func": self.GoToPage,
                "args": [self.data.get("addr1", "0")]    
            }
            toPageCallback2 = {
                "func": self.GoToPage,
                "args": [self.data.get("addr2", "0")]    
            }
            buttonImage = "textures/ui/myCustomBook/myButton"
            self.button1.SetDataBeforeShow(defaultImage=buttonImage, pressCallBack=toPageCallback1, text="按钮1")
            self.button2.SetDataBeforeShow(defaultImage=buttonImage, pressCallBack=toPageCallback2, text="按钮2")
            self.text1.SetDataBeforeShow(text=self.data.get("button1_text", ""))
            self.text2.SetDataBeforeShow(text=self.data.get("button2_text", ""))

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
            # 对 button1 设置大小后，将其中心对齐到页面的中心，将其上边界与 button1 的下边界对齐，然后往下移动5px
            self.text1.AlignCenterToX(pageCenter[0]).AlignTopToY(self.button1.Bottom()).MoveY(5)
            # 对 button2 设置大小后，将其中心对齐到页面的中心，将其上边界与 text1 的下边界对齐，然后往下移动10px
            self.button2.SetSize((40, 40)).AlignCenterToX(pageCenter[0]).AlignTopToY(self.text1.Bottom()).MoveY(10)
            # 对 text2 设置大小后，将其中心对齐到页面的中心，将其上边界与 button2 的下边界对齐，然后往下移动5px
            self.text2.AlignCenterToX(pageCenter[0]).AlignTopToY(self.button2.Bottom()).MoveY(5)
            return self
        else:
            print "in MyAddrPage Show: no data present"
            return self
        



        
