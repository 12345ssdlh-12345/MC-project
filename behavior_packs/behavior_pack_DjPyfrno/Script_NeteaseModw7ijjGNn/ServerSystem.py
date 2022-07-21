import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()
leveldatacomp = serverApi.GetEngineCompFactory().CreateExtraData(serverApi.GetLevelId())
commandcomp = serverApi.GetEngineCompFactory().CreateCommand(serverApi.GetLevelId())
timecomp = serverApi.GetEngineCompFactory().CreateTime(serverApi.GetLevelId())

class FarmServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print "服务端初始化"
        self.ListenForEvent("FarmMod", "ClientSystem", "create_data_ui",
                            self, self.CreateDataUi)
        #self.ListenForEvent("FarmMod", "ClientSystem", "buy_item",
        #                    self,self.PlayerBuyItem)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerAttackEntityEvent",
                            self,self.PlayerAttack)
        
        self.player_id = leveldatacomp.GetExtraData("player_id")
        self.player_money = leveldatacomp.GetExtraData("player_money")
        self.player_house = leveldatacomp.GetExtraData("player_house")
        #self.NotifyToClient('-8589934591', "create_data_ui", event)
        # 监听EntityPlaceBlockAfterServerEvent事件
        # self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
        #                    'EntityPlaceBlockAfterServerEvent',
        #                    self, self.Place_Furniture)
        # 监听ServerPlayerTryDestroyBlockEvent事件
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(),
                            'ServerPlayerTryDestroyBlockEvent',
                            self, self.Destroy_Corn)
        self.ListenForEvent("FarmMod", "ClientSystem", "buy_item",
                            self, self.PlayerBuyItem)
        # 使用中国版自定义方块方法制作的农作物列表
        self.netease_block_list = ["gszqq:corn_stage_2"]
        self.ListenForEvent(serverApi.GetEngineNamespace(),
                    serverApi.GetEngineSystemName(),
                    "ServerItemTryUseEvent",
                    self, self.Move)
        
    
    def CreateDataUi(self, playerid):########################################
        print "服务端CreateDataUiui"
        # 使用ExtraData存放数据，初始化游戏数据
        leveldatacomp.SetExtraData("player_money", 20000)
        leveldatacomp.SetExtraData("player_house", 1)
         # 将初始数据作为参数传到ClientSystem
        event = {"player_data_money": leveldatacomp.GetExtraData("player_money"), 
                "player_data_house": leveldatacomp.GetExtraData("player_house")}
        self.NotifyToClient('-8589934591', "create_data_ui", event)
    
    # 破坏方块时触发
    def Destroy_Corn(self, args):
        # 通过事件获取的方块坐标、名称
        x = args['x']
        y = args['y']
        z = args['z']
        blockname = args['fullName']
        player_id = args['playerId']
        # 创建方块状态接口
        #blockstatecomp = serverApi.GetEngineCompFactory().CreateBlockState(serverApi.GetLevelId())
        # 获取放置的方块状态
        #blockstate = blockstatecomp.GetBlockStates((x, y, z), 0)
        # 下方的逻辑和放置家具时一致，不过是将数据从+=1改为-+1
        if blockname == "gszqq:corn_stage_2":
            print "破坏方块，收获玉米"
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f收获玉米*5，金币+40\"}]}")
            leveldatacomp.SetExtraData("player_money", leveldatacomp.GetExtraData("player_money") + 40)
            event = {"player_data_money": leveldatacomp.GetExtraData("player_money")}
            self.NotifyToClient('-8589934591', "re_dataui", event)
        if blockname == "gszqq:xiangjiao_2":
            print "破坏方块，收获香蕉"
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f收获香蕉*10，金币+50\"}]}")
            leveldatacomp.SetExtraData("player_money", leveldatacomp.GetExtraData("player_money") + 50)
            event = {"player_data_money": leveldatacomp.GetExtraData("player_money")}
            self.NotifyToClient('-8589934591', "re_dataui", event)
        if blockname == "gszqq:qiezi_2":
            print "破坏方块，收获茄子"
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f收获茄子*5，金币+30\"}]}")
            leveldatacomp.SetExtraData("player_money", leveldatacomp.GetExtraData("player_money") + 30)
            event = {"player_data_money": leveldatacomp.GetExtraData("player_money")}
            self.NotifyToClient('-8589934591', "re_dataui", event)
        if blockname == "gszqq:bocai_2":
            print "破坏方块，收获菠菜"
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f收获菠菜*10，金币+20\"}]}")
            leveldatacomp.SetExtraData("player_money", leveldatacomp.GetExtraData("player_money") + 20)
            event = {"player_data_money": leveldatacomp.GetExtraData("player_money")}
            self.NotifyToClient('-8589934591', "re_dataui", event)
        if blockname == "gszqq:wandou_2":
            print "破坏方块，收获豌豆"
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f收获豌豆*20，金币+20\"}]}")
            leveldatacomp.SetExtraData("player_money", leveldatacomp.GetExtraData("player_money") + 20)
            event = {"player_data_money": leveldatacomp.GetExtraData("player_money")}
            self.NotifyToClient('-8589934591', "re_dataui", event)
    
    def PlayerAttack(self,args):
        print "攻击了"
        entityid = args["victimId"]
        print "实体id",entityid
        self.playername = args["playerId"]
        if entityid == '-511101106400':
            event = {"playerid": args["playerId"], "entityid": entityid,
                    "player_money": leveldatacomp.GetExtraData("player_money")}
            print "钱",leveldatacomp.GetExtraData("player_money")
            self.NotifyToClient(self.playername,"create_seed_shop_ui", event)
        if entityid == '-511101105979':
            event = {"playerid": args["playerId"], "entityid": entityid,
                     "player_money": leveldatacomp.GetExtraData("player_money"),"player_house": leveldatacomp.GetExtraData("player_house")}
            print "钱",leveldatacomp.GetExtraData("player_money")
            self.NotifyToClient(self.playername,"create_house_shop_ui", event)
    
    def PlayerBuyItem(self, args):
        print "玩家买到了"
        if args['buy_item']=="玉米":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f购买成功！玉米种子+1\"}]}")
        if args['buy_item']=="茄子":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f购买成功！茄子种子+1\"}]}")
        if args['buy_item']=="豌豆":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f购买成功！豌豆种子+1\"}]}")
        if args['buy_item']=="香蕉":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f购买成功！香蕉种子+1\"}]}")
        if args['buy_item']=="菠菜":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f购买成功！菠菜种子+1\"}]}")
        if args['buy_item']=="豪华别墅":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f恭喜！豪华别墅购买成功，开辟新地图\"}]}")
        if args['buy_item']=="温馨小屋":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f恭喜！温馨小屋购买成功，开辟新地图\"}]}")
        if args['buy_item']=="浪漫公寓":
            commandcomp.SetCommand(
                            "execute @a ~ ~ ~ tellraw @a {\"rawtext\":[{\"text\":\" §6§l【系统】 §r§f恭喜！浪漫公寓购买成功，开辟新地图\"}]}")
        leveldatacomp.SetExtraData("player_money", args["money"])
        player_id = args['playerid']  # 传过来的玩家id
        item_name = args['item']  # 传过来的实际商品名称
        if "house" in args:
            event = {"playerid": player_id, "player_data_money": args['money'],"player_data_house": args['house'] }
            leveldatacomp.SetExtraData("player_house", args["house"])
        if "house" not in args:
            event = {"playerid": player_id, "player_data_money": args['money']}
        self.NotifyToClient(player_id, "re_dataui", event)
        serverApi.GetEngineCompFactory().CreateItem(player_id).SpawnItemToPlayerInv(  # 发放物品
            {
                'newItemName': item_name,
                'count': 1
            },
            player_id
        )
    
    def Move(self,args):
        print "玩家传送"
        if args['itemDict']['newItemName']=="gszqq:key1":
            print "玩家传送key1"
            comp = serverApi.GetEngineCompFactory().CreateDimension(args['playerId'])
            comp.ChangePlayerDimension(0, (244,65,296))
        if args['itemDict']['newItemName']=="gszqq:key2":
            print "玩家传送key2"
            comp = serverApi.GetEngineCompFactory().CreateDimension(args['playerId'])
            comp.ChangePlayerDimension(0, (247,64,296))
        if args['itemDict']['newItemName']=="gszqq:key3":
            print "玩家传送key3"
            comp = serverApi.GetEngineCompFactory().CreateDimension(args['playerId'])
            comp.ChangePlayerDimension(0, (344,65,310))

