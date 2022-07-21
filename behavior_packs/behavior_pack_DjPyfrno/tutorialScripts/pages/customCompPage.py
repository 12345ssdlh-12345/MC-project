#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取页面基类 BasePage
BasePage = bookManager.GetBasePageCls()
# 引入自定义的组件类 MyCustomComp
from tutorialScripts.comps.customComp import MyCustomComp

class MyCustomCompPage(BasePage):
    """
        自定义的页类，同时包含自定义的组件
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
        self.customComp1 = MyCustomComp()
        self.customComp2 = MyCustomComp()

        # 调用AddComps接口添加所有定义了的组件
        self.AddComps(self.customComp1, self.customComp2)

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
            4. 对组件进行排版（通过调用组件的排版API）。           
        """
        if self.data:
            # 为每个组件注入数据，data中的键值对应json文件中的页面属性值
            customComp1_data = self.data.get("customComp1", None)
            customComp2_data = self.data.get("customComp2", None)

            if customComp1_data:
                # 通过Dict的get方法，可以为一些属性赋予默认值
                self.customComp1.SetDataBeforeShow(customComp1_data["image"], customComp1_data["text"], \
                    tuple(customComp1_data.get("textColor", bcf.Colors.TextDefault)), \
                    customComp1_data.get("textSize", bcf.TextSize.content)
                    )

            if customComp2_data:
                self.customComp2.SetDataBeforeShow(customComp2_data["image"], customComp2_data["text"], \
                    tuple(customComp2_data.get("textColor", bcf.Colors.TextDefault)), \
                    customComp2_data.get("textSize", bcf.TextSize.content)
                    )

            # 执行父类的Show方法
            BasePage.Show(self)

            # 重置所有组件相对页面的位置，保证每次调用Show的时候组件的排版都是相对于页面的原点
            self.ResetCompsPosition()   
            # 获取该页面的中心坐标和大小，方便后面使用
            pageCenter = self.Center()    
            pageSize = self.GetSize() 
            
            # 布局自己的组件，组件在调用Align以及Move方法前需要先调用SetSize方法，因为这些方法都是基于GetSize来计算的。
            # 对组件进行排版，让组件 customComp1 排版在左上方， 让组件 customComp2 排版在右下方
            if customComp1_data:
                size = customComp1_data.get("size", (60, 60))
                # 对 customComp1 设置大小后，将其左边界对齐到页面的左边界，将其上边界与 页面 的上边界对齐
                self.customComp1.SetSize(size).AlignLeftToX(self.Left()).AlignTopToY(self.Top())
            if customComp2_data:
                size = customComp2_data.get("size", (60, 60))
                # 对 customComp2 设置大小后，将其右边界对齐到页面的右边界，将其下边界与 页面 的下边界对齐
                self.customComp2.SetSize(size).AlignRightToX(self.Right()).AlignBottomToY(self.Bottom())          

            return self
        else:
            print "in MyCustomCompPage Show: no data present"
            return self
        



        
