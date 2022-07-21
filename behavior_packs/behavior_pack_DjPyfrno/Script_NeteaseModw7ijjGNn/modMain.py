# -*- coding: utf-8 -*-

from common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="NeteaseModw7ijjGNn", version="0.0.1")
class NeteaseModw7ijjGNn(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def NeteaseModw7ijjGNnServerInit(self):
     #   serverApi.RegisterSystem("FarmMod", "ServerBlockListenerServer",
     #                            "Script_NeteaseModw7ijjGNn.server.blockListener.Main")
        serverApi.RegisterSystem("FarmMod", "ServerSystem",
                                 "Script_NeteaseModw7ijjGNn.ServerSystem.FarmServerSystem")
    @Mod.DestroyServer()
    def NeteaseModw7ijjGNnServerDestroy(self):
        pass

    @Mod.InitClient()
    def NeteaseModw7ijjGNnClientInit(self):
        clientApi.RegisterSystem("FarmMod", "ClientSystem",
                                 "Script_NeteaseModw7ijjGNn.ClientSystem.FarmClientSystem")

    @Mod.DestroyClient()
    def NeteaseModw7ijjGNnClientDestroy(self):
        pass
