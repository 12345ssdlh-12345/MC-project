#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取页面基类 BasePage
BasePage = bookManager.GetBasePageCls()
# 获取预设组件类 TextComp
TextComp = bookManager.GetTextCompCls()
# 获取预设组件类 ImageComp
ImageComp = bookManager.GetImageCompCls()

class MyNoTitlePage(BasePage):
    """
        自定义的页类
    """
    def __init__(self, size = None, position = None):
        """"
            编写该接口需按照如下编写。
            1. 先调用父类的同名方法。
            2. 定义需要用到的组件。
            3. 调用AddComps接口添加所有组件。
        """
        # 调用父类__init__方法
        BasePage.__init__(self, size, position)
        
        # 实例化需要用到的组件
        self.testTitle = TextComp(bcf.TextAlign.Fit_Center)  # 使用文本组件存储显示自定义属性"testTitle""
        self.content1 = TextComp(bcf.TextAlign.Left)  # 使用文本组件存储显示自定义属性"content1""  
        self.image = ImageComp()  # 使用图片组件存储显示自定义属性"image""    
        self.content2 = TextComp(bcf.TextAlign.Left)  # 使用文本组件存储显示自定义属性"content2""  

        # 调用AddComps接口添加所有定义了的组件
        self.AddComps(self.testTitle, self.content1, self.image, self.content2)

        # 照应SetData方法
        self.data = None


    def SetData(self, data):
        """
            书本在调用Show之前会调用该方法将json中的数据打包成Dict变量"data"作为参数传进来。
            建议是将数据存储下来然后在Show方法中进行读取。
        """
        # 存储各个组件的数据
        self.data = data
        return self

    def Show(self):
        """
            书本向页面传递数据后调用该接口，这里负责为每个组件填充数据并且排版它们的位置。
            编写该接口需按照如下编写。
            1. 向所有组件注入数据。
            2. 调用父类的同名方法。
            3. 重置所有组件相对于页面的位置。
            4. 对组件进行排版（通过调用组件的排版API，每个API的解释见“03-组件API”）。           
        """
        if self.data:
            # 为每个组件注入数据，data中的键值对应json文件中的页面属性值
            self.testTitle.SetDataBeforeShow(self.data["testTitle"], bcf.TextSize.title)
            self.content1.SetDataBeforeShow(self.data["content1"], bcf.TextSize.content)
            self.content2.SetDataBeforeShow(self.data["content2"], bcf.TextSize.content)
            self.image.SetDataBeforeShow(self.data["image"])

            # 执行父类的Show方法，该方法会依次调用会所有组件的Show方法
            BasePage.Show(self)
            # 重置所有组件相对页面的位置，保证每次调用Show的时候组件的排版都是相对于页面的原点
            self.ResetCompsPosition()   
            # 获取该页面的中心坐标和大小，方便后面使用
            pageCenter = self.Center()    
            pageSize = self.GetSize() 
                   
            # 布局自己的组件，组件在调用Align以及Move方法前需要先调用SetSize方法，因为这些方法都是基于GetSize来计算的。
            # testTitle 是Fit类型文本，会根据文本内容来调整自己的大小，无需调用SetSize。将其中心对齐到页面的中心，将其上边界与 页面 的上边界对齐，然后往下移动4px
            self.testTitle.AlignCenterToX(pageCenter[0]).AlignTopToY(self.Top()).MoveY(4)
            # 对 content1 设置大小后，将其左边界对齐到页面的左边界，将其上边界与 testTitle 的下边界对齐，然后往下移动5px
            self.content1.SetSize((pageSize[0], 20)).AlignLeftToX(self.Left()).AlignTopToY(self.testTitle.Bottom()).MoveY(5)
            # 对 image 设置大小后，将其左中心对齐到页面的中心，将其上边界与 content1 的下边界对齐，然后往下移动5px
            self.image.SetSize((80, 80)).AlignCenterToX(pageCenter[0]).AlignTopToY(self.content1.Bottom()).MoveY(5)
            # 对 content2 设置大小后，将其左边界对齐到页面的左边界，将其上边界与 image 的下边界对齐，然后往下移动5px
            self.content2.SetSize((pageSize[0], 40)).AlignLeftToX(self.Left()).AlignTopToY(self.image.Bottom()).MoveY(5)
            
            return self
        else:
            print "in MyNoTitlePage Show: no data present"
            return self
        



        
