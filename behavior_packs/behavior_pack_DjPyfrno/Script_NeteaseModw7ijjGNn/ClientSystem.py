# -*- coding: utf-8 -*-


import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
playername = clientApi.GetLocalPlayerId()
timercomp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
cameracomp = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId())

class FarmClientSystem(ClientSystem):

    def __init__(self, namespace, systemName):
        super(FarmClientSystem, self).__init__(namespace, systemName)
        self.playerid = clientApi.GetLocalPlayerId()
        print "本地id" , self.playerid
        namespace = clientApi.GetEngineNamespace()
        system_name = clientApi.GetEngineSystemName()
        self.ListenForEvent(namespace, system_name,
                            'UiInitFinished', self, self.ui_init)
        self.ListenForEvent("FarmMod", "ServerSystem", "re_dataui",
                            self, self.Re_DataUI)                    
        # 监听由ServerSystem发送过来的事件
        self.ListenForEvent("FarmMod", "ServerSystem", "create_data_ui",
                            self, self.CreateDataUI)
        self.ListenForEvent("FarmMod", "ServerSystem", "create_seed_shop_ui",
                            self, self.Create_Seed_Shop_UI)
        self.ListenForEvent("FarmMod", "ServerSystem", "create_house_shop_ui",
                            self, self.Create_House_Shop_UI)

    def CreateDataUI(self,event):
        print "client_CreateDataUI"
        # 创建UI
        clientApi.CreateUI("Farm","data_ui",{"isHud":1})
        clientApi.PushScreen("Farm","GameBook")
        # 执行更新UI数据的函数
        self.Re_DataUI(event)


    def Create_Seed_Shop_UI(self,event):
        print "Create_Seed_Shop_UI"
        self.ui = clientApi.PushScreen("Farm","new_shop")
        self.ui.money=event["player_money"]

    def Create_House_Shop_UI(self,event):
        print "Create_House_Shop_UI"
        self.house_ui = clientApi.PushScreen("Farm","house_shop")
        self.house_ui.money=event["player_money"]
        self.house_ui.house=event["player_house"]
    
    def Re_DataUI(self,event):
        print "Re_DataUI",event
        # 获取UI实例
        self.data_ui = clientApi.GetUI("Farm","data_ui")
        # 如果传过来的参数有player_data_coin则更新UI中的coin
        if "player_data_money" in event:
            self.data_ui.money = event["player_data_money"]
        # 如果传过来的参数有player_data_house则更新UI中的house
        if "player_data_house" in event:
            self.data_ui.house = event["player_data_house"]

    def ui_init(self,args):
        print "ui_init"
        clientApi.RegisterUI("Farm", "data_ui", "Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen", "data_ui.main")
        clientApi.RegisterUI("Farm","new_shop","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","new_shop.main")
        clientApi.RegisterUI("Farm","house_shop","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","house_shop.main")
        clientApi.RegisterUI("Farm","GameBook","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","GameBook.main")
        clientApi.RegisterUI("Farm","GameBook_1","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","GameBook_1.main")
        clientApi.RegisterUI("Farm","GameBook_2","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","GameBook_2.main")
        clientApi.RegisterUI("Farm","GameBook_3","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","GameBook_3.main")
        clientApi.RegisterUI("Farm","GameBook_4","Script_NeteaseModw7ijjGNn.uiscreen.FarmUIScreen","GameBook_4.main")
        self.NotifyToServer("create_data_ui",{"player_id":self.playerid})