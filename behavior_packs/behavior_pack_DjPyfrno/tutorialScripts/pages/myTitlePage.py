#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取预设页面类 TitlePage
TitlePage = bookManager.GetTitlePageCls()
# 获取预设组件类 TextComp
TextComp = bookManager.GetTextCompCls()
# 获取预设组件类 ImageComp
ImageComp = bookManager.GetImageCompCls()


class MyTitlePage(TitlePage):

    def __init__(self, size = None, position = None):
        # 调用父类同名方法，TitlePage 会自动添加标题组件以及提供标题组件注入数据的方法，排版的方法。
        TitlePage.__init__(self, size, position)
        self.content1 = TextComp(bcf.TextAlign.Left)    
        self.image = ImageComp()    
        self.content2 = TextComp(bcf.TextAlign.Left)    
        self.AddComps(self.content1, self.image, self.content2)

    def SetData(self, data):
        # TitlePage 会调用 self.data 从中获取json数据。
        self.data = data
        return self

    def Show(self):
        if self.data:
            # 注入数据，先给标题注入数据
            self.SetTitleData()
            # 再给自己的其他组件注入数据
            self.content1.SetDataBeforeShow(self.data["content1"], bcf.TextSize.content)
            self.content2.SetDataBeforeShow(self.data["content2"], bcf.TextSize.content)
            self.image.SetDataBeforeShow(self.data["image"])
            # 执行基础类的方法获取节点并显示出来
            TitlePage.Show(self)
            # 排版位置，先重置所有组件相对页面的位置，保证每次调用Show的时候组件的Move都是相对于Page的原点
            self.ResetCompsPosition()   
            pageCenter = self.Center()    
            pageSize = self.GetSize() 
            
            # 排版标题并获取内容开始的坐标y值
            content_begin = self.LayoutTitle()
            
            # 布局自己的组件，组件在调用Align以及Move方法前需要先调用SetSize方法，因为这些方法都是基于GetSize来计算的。
            # 对 content1 设置大小后，将其左边界对齐到页面的左边界，将其上边界与 标题 的下边界对齐，然后往下移动5px
            self.content1.SetSize((pageSize[0], 20)).AlignLeftToX(self.Left()).AlignTopToY(content_begin).MoveY(5)
            # 对 image 设置大小后，将其中心对齐到页面的中心，将其上边界与 content1 的下边界对齐，然后往下移动5px
            self.image.SetSize((80, 80)).AlignCenterToX(pageCenter[0]).AlignTopToY(self.content1.Bottom()).MoveY(5)
            # 对 content2 设置大小后，将其左边界对齐到页面的左边界，将其上边界与 image 的下边界对齐，然后往下移动5px
            self.content2.SetSize((pageSize[0], 40)).AlignLeftToX(self.Left()).AlignTopToY(self.image.Bottom()).MoveY(5)
            return self
        else:
            print "in MyTitlePage Show: no data present"
            return self
        



        
