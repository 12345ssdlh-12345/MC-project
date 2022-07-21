#-*- coding: UTF-8 -*- 

import mod.client.extraClientApi as clientApi
# 获取书本管理对象，详细用法见“05-常见脚本对象”
bookManager = clientApi.GetBookManager()
# 获取书本配置常量，详细API见“05-常见脚本对象”
bcf = bookManager.GetBookConfig()
# 获取组件基类 BaseComp
BaseComp = bookManager.GetBaseCompCls()

class MyRecyleToggle(BaseComp):
    """
        自定义的书本可回收组件
        主要实现功能： 组件会一直保存自己的状态，当玩家点击该toggle按钮后，并且进行翻页面跳转页面等操作，回来再显示页面的时候仍然是对应的状态
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
        # 注意最后一个参数，这里我们使用回收组件
        BaseComp.__init__(self, "CustomMod:MyRecyleToggle", "RecycleComps.main", "toggleBtn", True)
        
        self.on_state = True    # 自己保存自己当前的状态，不依赖reset来复原
        self.has_inited = False # 防止每次 SetDataBeforeShow 的时候覆盖自己当前的状态

        # 记录下需要用到的子节点路径
        self.press_np = "/pressed"
        self.hover_np = "/hover"
        self.default_np = "/default"
        self.text_np = "/button_label"
        # 记录下要使用到的图片
        self.off_image = "textures/items/toggle_off"
        self.on_image = "textures/items/toggle_on"


    def SetDataBeforeShow(self, onState):
        """
            页面在调用组件的Show之前默认会先调用该方法进行数据的存储
            建议是将数据存储下来然后在Show方法中进行读取。
        """       
        if not self.has_inited:
            # 从json data中获取数值作为初始值，之后不会再使用该数值
            self.on_state = onState
            self.has_inited = True
        return self
    
    def SetImage(self, imagePath):
        self.GetRootUINode().GetChildByPath(self.default_np).asImage().SetSprite(imagePath)
        self.GetRootUINode().GetChildByPath(self.hover_np).asImage().SetSprite(imagePath)
        self.GetRootUINode().GetChildByPath(self.default_np).asImage().SetSprite(imagePath)
        return self

    def SwitchToggle(self, args):
        if self.on_state:
            self.on_state = False
            self.SetImage(self.off_image)
        else:
            self.on_state = True
            self.SetImage(self.on_image)
        return self

    def BindEvents(self):
        btn = self.GetRootUINode().asButton()
        btn.AddTouchEventParams({"isSwallow":True})
        btn.SetButtonTouchUpCallback(self.SwitchToggle)
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
        # 绑定方法
        self.BindEvents()
        # 判断当前的状态是否为开启状态
        if self.on_state:
            self.SetImage(self.on_image)
        else:
            self.SetImage(self.off_image)
                                
        return self

    def Reset(self):
        # 组件自己记录自己的状态，在每次Show的时候从自己的状态中读取，所以无需再复原控件节点的属性。
        return self