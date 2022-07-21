# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import re

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

class FarmUIScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.clientsystem = clientApi.GetSystem("FarmMod", "ClientSystem")  # 获取客户端实例
        #self.coin =0  # 定义玩家的钱数
        #self.house =0
        self.index = -1 #按钮的index值
        self.house_index= -1
        self.seed_text = [
			{
				"itemtext":"玉米", #商品的名称，
				"information":"品种：玉米\n生长周期：3\n价格：5", #商品的详细信息，展示在UI右侧
				"coin": 5, #购买商品的价格
				"itemname":"gszqq:corn_seed" #用于读取实际商品以给予玩家
			},
			{
				"itemtext": "茄子",
				"information": "品种：茄子\n生长周期：3\n价格：10",
				"coin": 10,
				"itemname": "gszqq:qiezi"
			},
			{
				"itemtext": "香蕉",
				"information": "品种：香蕉\n生长周期：3\n价格：15",
				"coin": 15,
				"itemname": "gszqq:xiangjiao"
			},
			{
				"itemtext": "豌豆",
				"information": "品种：豌豆\n生长周期：3\n价格：5",
				"coin": 5,
				"itemname": "gszqq:wandou"
			},
			{
				"itemtext": "菠菜",
				"information": "品种：菠菜\n生长周期：3\n价格：5",
				"coin": 5,
				"itemname": "gszqq:bocai"
			}
		]
        self.house_text = [
			{
				"itemtext":"豪华别墅", #商品的名称，
				"information":"豪华装修，皇家牌面\n10000金币", #商品的详细信息，展示在UI右侧
				"coin": 10000, #购买商品的价格
				"itemname":"gszqq:key2" #用于读取实际商品以给予玩家
			},
			{
				"itemtext": "温馨小屋",
				"information": "温馨木屋，复古情调\n2000金币",
				"coin": 2000,
				"itemname": "gszqq:key1"
			},
			{
				"itemtext": "浪漫公寓",
				"information": "艺术造型，极具现代化气息\n5000金币",
				"coin": 5000,
				"itemname": "gszqq:key3"
			}
		]
   
    # 绑定字符串，返回self.money（money变化时通过创建ui实例修改参数）
    @ViewBinder.binding(ViewBinder.BF_BindString, "#money_text")
    def player_money_text(self):
        #print "钱数1",self.money
        return str(self.money)
    
	# 绑定字符串，返回购买房子数
    @ViewBinder.binding(ViewBinder.BF_BindString, "#house_text")
    def player_house_text(self):
        #print "房子数"
        return str(self.house)

    #关闭按钮的绑定函数,按钮按下再松开后触发
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_close_button(self,args):
        print "按关闭了！"
        clientApi.PopScreen()
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def CloseButton1(self,args):
        print "CloseButton1"
        clientApi.PopScreen()
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def CloseButton2(self,args):
        print "CloseButton2"
        clientApi.PopScreen()
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def CloseButton3(self,args):
        print "CloseButton3"
        clientApi.PopScreen()
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def CloseButton4(self,args):
        print "CloseButton4"
        clientApi.PopScreen()
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def CloseButton5(self,args):
        print "CloseButton5"
        clientApi.PopScreen()

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_yvmi_button(self,args):
        print "查看了玉米"
        self.index=0

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_xiangjiao_button(self,args):
        print "查看了香蕉"
        self.index=2
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_qiezi_button(self,args):
        print "查看了茄子"
        self.index=1
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_zhusun_button(self,args):
        print "查看了豌豆"
        self.index=3
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_pingguo_button(self,args):
        print "查看了菠菜"
        self.index=4
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_bieshu_button(self,args):
        print "查看了别墅"
        self.house_index=0
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_xiaowu_button(self,args):
        print "查看了小屋"
        self.house_index=1
    
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def clicked_gongyv_button(self,args):
        print "查看了公寓"
        self.house_index=2

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def PageTurnButton1(self,args):
        print "PageTurnButton1"
        clientApi.PopScreen()
        clientApi.PushScreen("Farm","GameBook_1")
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def PageTurnButton2(self,args):
        print "PageTurnButton2"
        clientApi.PopScreen()
        clientApi.PushScreen("Farm","GameBook_2")
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def ReturnButton3(self,args):
        print "ReturnButton3"
        clientApi.PopScreen()
        clientApi.PushScreen("Farm","GameBook_3")
    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def ReturnButton4(self,args):
        print "ReturnButton4"
        clientApi.PopScreen()
        clientApi.PushScreen("Farm","GameBook_4")

    #绑定字符串，给商品信息添加对应的描述
    @ViewBinder.binding(ViewBinder.BF_BindString,"#shop_information")
    def binding_shop_information(self):
        return self.seed_text[self.index]["information"] #返回对应index的描述信息

    @ViewBinder.binding(ViewBinder.BF_BindString,"#house_information")
    def binding_house_information(self):
        return self.house_text[self.house_index]["information"] #返回对应index的描述信息

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def buy_button_clicked(self,args):
        print "点击购买了"
        if self.index == -1:
            print "玩家还没选物品"
            return
        price = self.seed_text[self.index]['coin']
        print "他想买的东西价值:",price
        print "你有的钱数：",self.money
        if self.money >= price:
            self.money -= price
            print "买完以后你还剩：",self.money
			#向服务端通信，将玩家id，剩余钱数，以及购买的实际物品作为参数传送过去
            self.clientsystem.NotifyToServer("buy_item",{"playerid":clientApi.GetLocalPlayerId(),"money":self.money,"buy_item":self.seed_text[self.index]["itemtext"],"item":self.seed_text[self.index]["itemname"]})
        else:
            print "你买不起"

    @ViewBinder.binding(ViewBinder.BF_ButtonClickUp)
    def buy_house_button_clicked(self,args):
        print "点击购买了"
        if self.house_index == -1:
            print "玩家还没选物品"
            return
        price = self.house_text[self.house_index]['coin']
        print "他想买的东西价值:",price
        print "你有的钱数：",self.money
        if self.money >= price:
            self.money -= price
            self.house +=1
            print "买完以后你还剩：",self.money
            print "买完以后房子：",self.house
			#向服务端通信，将玩家id，剩余钱数，以及购买的实际物品作为参数传送过去
            self.clientsystem.NotifyToServer("buy_item",{"playerid":clientApi.GetLocalPlayerId(),"money":self.money,"house":self.house,"buy_item":self.house_text[self.house_index]["itemtext"],"item":self.house_text[self.index]["itemname"]})
        else:
            print "你买不起"