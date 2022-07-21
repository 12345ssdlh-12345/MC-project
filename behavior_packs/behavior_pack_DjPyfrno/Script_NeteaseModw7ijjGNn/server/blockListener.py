# -*- coding: UTF-8 -*-
from mod.server.system.serverSystem import ServerSystem
from mod.common.minecraftEnum import ItemPosType
import mod.server.extraServerApi as serverApi


class Main(ServerSystem):

    def __init__(self, namespace, system_name):
        # 继承父类
        ServerSystem.__init__(self, namespace, system_name)
        namespace = serverApi.GetEngineNamespace()
        system_name = serverApi.GetEngineSystemName()
        # 监听交互方块事件
        self.ListenForEvent(namespace, system_name,
                            'ServerBlockUseEvent', self, self.using_item)
        # 根据文档描述，原版方块需要通过添加进交互方块的白名单内才能触发ServerBlockUseEvent
        block_comp = serverApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(serverApi.GetLevelId())
        # 在地图的方块结构里，一共受到锄头影响的两种地形方块是
        self.blocked_list = ["minecraft:grass", "minecraft:grass_path"]
        for block_name in self.blocked_list:
            # 加入白名单
            block_comp.AddBlockItemListenForUseEvent(block_name)
        block_comp.AddBlockItemListenForUseEvent('minecraft:standing_sign:*')
        # 储存资源点坐标
        self.resources_pos = [
            (73, 64, 57),
            (51, 63, 101),
            (82, 68, 136),
            (198, 65, 102),
            (82, 68, 136)
        ]
        # 结构名称
        self.resource_identifier = 'design:resource'
        # 添加一个60秒重置资源点的定时任务
        game_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        game_comp.AddRepeatedTimer(60.0, self.resource_placed)

    # 交互方块事件
    def using_item(self, event):
        # 获取玩家ID
        player_id = event['playerId']
        # 创建玩家的物品接口
        item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
        # 获取玩家手持物品信息
        carried_item = item_comp.GetPlayerItem(ItemPosType.CARRIED, 0, True)
        # 获取事件里交互的方块类型
        block_name = event['blockName']
        x = event['x']
        y = event['y']
        z = event['z']
        # 判断方块类型是否是土径或草地，并判断玩家手持物品是否是石锄
        if carried_item and carried_item['newItemName'] == 'minecraft:stone_hoe' and block_name in self.blocked_list:
            # 取消交互
            event['cancel'] = True
        # 判断是否是告示牌
        if block_name == 'minecraft:standing_sign':
            block_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
            text = block_comp.GetSignBlockText((x, y, z))
            # 需求列表
            requirement = {}
            # 结构名称
            structure_name = ''
            # 结构放置位置
            structure_pos = ()
            # 小屋升级方块坐标
            if '升级小屋' in text:
                requirement = {'minecraft:log': 10, 'minecraft:stone': 5}
                structure_name = 'design:home'
                structure_pos = (76, 66, 80)
            # 畜牧场升级方块坐标
            elif '升级畜牧场' in text:
                requirement = {'minecraft:log': 20, 'minecraft:stone': 10}
                structure_name = 'design:farm'
                structure_pos = (169, 66, 83)
            result, items = self.can_upgrade_structure(player_id, requirement)
            # 是否满足要求
            if result and structure_pos and structure_name and requirement:
                """
                使用字典推导式，下方等价于
                item_dict_map = {}
                for index in range(len(item_dict_list)):
                    item_dict_map[(ItemPosType.INVENTORY, index)] = item_dict_list[index]
                """
                item_dict_map = {(ItemPosType.INVENTORY, index): items[index] for index in range(len(items))}
                item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
                # 设置玩家的全部槽内物品
                item_comp.SetPlayerAllItems(item_dict_map)
                game_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
                # 放置家
                game_comp.PlaceStructure(None, structure_pos, structure_name)
                # 清除木牌
                block_comp.SetBlockNew((x, y, z), {
                    'name': 'minecraft:air'
                }, 0, 0)

    def resource_placed(self):
        # 创建放置结构的接口
        game_comp = serverApi.GetEngineCompFactory().CreateGame(serverApi.GetLevelId())
        for pos in self.resources_pos:
            # 放置资源点结构
            game_comp.PlaceStructure(None, pos, self.resource_identifier)

    def can_upgrade_structure(self, player_id, requirement):
        # type: (str, dict) -> (bool, list)
        """
        :param player_id: 玩家ID
        :param requirement: 物品需求，例->{"minecraft:log": 10, "minecraft:stone": 5}
        :return (bool, list): 是否可以升级建筑，玩家背包信息
        """
        # 创建玩家的物品接口
        item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
        # 获取玩家背包的所有物品
        item_dict_list = item_comp.GetPlayerAllItems(ItemPosType.INVENTORY)
        # 通过枚举列表内的信息，遍历列表下标与物品信息
        for index, item_dict in enumerate(item_dict_list):
            # 如果该槽存在物品且物品在所需物品字典内，并且所需物品对应的数量大于0时
            if item_dict and item_dict['itemName'] in requirement and requirement[item_dict['itemName']] > 0:
                temp = item_dict['count']
                # 该槽物品数量扣去所需物品剩余数量
                temp -= requirement[item_dict['itemName']]
                # 如果该槽的物品数量不足以吃掉所需物品剩余数量
                if temp < 0:
                    # 设置该槽的物品数量为0，即代表该槽为空
                    item_dict['count'] = 0
                    # 扣去临时贮存的物品数量
                    requirement[item_dict['itemName']] -= temp
                    # 直接跳过后面代码进入下一次循环
                    continue
                # 否则，扣除对应槽位的物品数量
                item_dict['count'] = temp
                # 清零所需物品
                requirement[item_dict['itemName']] = 0
        # 返回是否满足升级条件，以及清零所需物品后的背包情况
        return not all(requirement.values()), item_dict_list
