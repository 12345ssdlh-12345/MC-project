#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取组件基类 BaseComp
BaseComp = bookManager.GetBaseCompCls()

class MyCustomComp(BaseComp):
    """
        自定义的书本组件类
    """    
    def __init__(self):
        """
            编写该接口需按照如下编写。
            1. 先调用父类的同名方法。
            2. 定义自定义的属性           
        """
        # 调用父类__init__方法，该方法会注册书本自定义组件名称，因此该方法只能调用一次（一个组件绑定一个控件节点）。
        # 第1个参数为组件的注册名称，为了防止重名，建议名字格式为 'mod名称:任意名称'，最好就是带“Comp”后缀。
        # 第2个参数为组件所封装的UI控件所在的json文件名+'.main'
        # 第3个参数为组件所封装的UI控件节点名称
        # 通过第2，3个参数可以让组件定位到所要封装的UI控件节点，更详细的内容可见 "组件API" 章节。
        BaseComp.__init__(self, "CustomMod:MyCustomComp", "CustomComp.main", "testComp")

        # 定义自定义的属性，这些都是向页面暴露的属性
        self.text = None                # 组件的文本字符串，类型为str
        self.textSize = None            # 组件的文本大小，类型为int
        self.textColor = None           # 组件的文本颜色，类型为tuple(4)
        self.image = None               # 组件的图片路径，类型为str


    def SetDataBeforeShow(self, image, text, textColor, textSize):
        """
            页面在调用组件的Show之前默认会先调用该方法进行数据的存储
            建议是将数据存储下来然后在Show方法中进行读取。
        """       
        # 存储页面传过来的数据
        self.text = text
        self.textSize = textSize
        self.textColor = textColor
        self.image = image   
 
        return self


    def Show(self):
        """
            页面向组件传递数据后调用该接口，组件在这里对UIControl节点进行操作。
            编写该接口需按照如下编写。
            1. 调用父类的同名方法。
            2. 按照特定逻辑处理你的UIControl节点         
        """        
        # 执行父类的Show方法，执行该方法后组件才能得到对应的UI控件节点并用_node_属性指向它。
        BaseComp.Show(self)

        # 往UI控件节点填充数据，_node_为组件所对应的UI控件节点（本demo中为 testComp，即__init__方法中的第3个参数）。
        textNode = self.GetRootUINode().GetChildByPath("/text").asLabel()
        # 如果是LabelUIControl节点，设置文本和字体大小时需要分别调用 SetNodeText 和 SetTextFontSize，具体可见 "组件API" 章节。
        self.SetNodeText(textNode, self.text).SetNodeTextFontSize(textNode, 10, self.textSize)
        textNode.SetTextColor(self.textColor)
        imageNode = self.GetRootUINode().GetChildByPath("/image").asImage()         
        imageNode.SetSprite(self.image)                                    
        return self

