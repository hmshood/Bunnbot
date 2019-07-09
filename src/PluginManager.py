# Python 3.6
# (c) Alexander J. (KingCrazy) 2018

import imp
import importlib
import os
import asyncio
import sys
from src import Bytes
from src import Bunn as B
from src import Consts as C
from src import PermissionAuthority as PA
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(2)

plugin_folder = "./plugins"
main_module = "__init__"
permission_authority = PA.PermissionAuthority()
permissions_file = "permissions.json"

class PluginManager():
    def __init__(self):
        self.plugins = []

        try:
            self.plugins = self.get_plugins()

            for i in self.plugins:
                i.init()
        except:
            raise

    def get_plugins(self):
        plugins = []
        plugin_name = ""
        plugin_files = os.listdir(plugin_folder)
        for i in plugin_files:
            path = os.path.join(plugin_folder, i)

            self.load_permissions(path,False)

            if not os.path.isdir(path) or not main_module + ".py" in os.listdir(path):
                continue

            info = importlib.import_module("plugins." +i)
            #print(info.__name__)
            plugins.append(info)
            #info = importlib.machinery.PathFinder().find_spec(main_module, [path])
            #plug = self.load_plugin(info)
            #self.plugins.append(plug)
            #info.loader.exec_module(plug)
            #plugins.append(info)#{"name":i,"info":info})
            print("Loaded plugin: {}".format(i))
        return plugins

    def load_plugin(self, plugin):
        return importlib.util.module_from_spec(plugin)

    def load_permissions(self,path,override):
        if permissions_file in os.listdir(path):
            print("Loading permissions file for {}".format(path))
            permission_authority.load_permissions(os.path.join(path, permissions_file),override)
        else:
            print("Warning: Permission file not found for {}".format(path))

    async def async_load_permissions(self,path,override):
        if permissions_file in os.listdir(path):
            print("Loading permissions file for {}".format(path))
            await permission_authority.async_load_permissions(os.path.join(path, permissions_file),override)
        else:
            print("Warning: Permission file not found for {}".format(path))

    async def async_reload_plugins(self):
        try:
            for i in self.plugins:
                importlib.reload(i)
                path = os.path.join(plugin_folder, i.__name__.split(".")[1])
                await self.async_load_permissions(path,True)
                i.init()
            print("Plugins successfully reloaded")
        except:
            print("Plugins failed to reload")
            raise

    async def async_reload_plugin(self,plugin_name):
        for i in self.plugins:
            if i.__name__ == "plugins."+plugin_name:
                importlib.reload(i)
                path = os.path.join(plugin_folder, i.__name__.split(".")[1])
                await self.async_load_permissions(path,True)
                i.init()
                print("Plugin {} successfully reloaded".format(plugin_name))
                return
        print("Plugin {} not found".format(plugin_name))

    async def async_load_plugin(self, plugin):
        return importlib.util.module_from_spec(plugin)

    async def on_update(self):
        while(True):
            for i in self.plugins:
                try:
                    if ("on_update" in dir(i)):
                        asyncio.ensure_future(i.on_update())
                except:
                    print("Unexpected plugin error: " + sys.exc_info()[0])
                    pass
            await asyncio.sleep(0.1)

    async def on_event(self, code, msg):
        has_authority = False    

        if (code == Bytes.b_ChatMessage and msg.message[0] == C.command_char):
            perm_level = await permission_authority.get_permission_level(msg)
            if (await permission_authority.check_permissions(msg.message,perm_level)):
                has_authority = True
            

        for i in self.plugins:
            try:
                if (code == Bytes.b_Ban and "on_ban" in dir(i)):
                    asyncio.ensure_future(i.on_ban(msg))
                if (code == Bytes.b_ChatMessage):
                    if (msg.message[0] == C.command_char):
                        if ("on_command" in dir(i) and has_authority == True):
                            await asyncio.sleep(0.1)
                            asyncio.ensure_future( i.on_command(msg))
                    if ("on_message" in dir(i)):
                        asyncio.ensure_future( i.on_message(msg))
                if (code == Bytes.b_ClearHistory and "on_clear_history" in dir(i)):
                    asyncio.ensure_future( i.on_clear_history(msg))
                if (code == Bytes.b_ClearUserMessages and "on_clear_user_messages" in dir(i)):
                    asyncio.ensure_future( i.on_clear_user_messages(msg))
                if (code == Bytes.b_Control and "on_control" in dir(i)):
                    asyncio.ensure_future( i.on_control(msg))
                if (code == Bytes.b_Kick and "on_kick" in dir(i)):
                    asyncio.ensure_future( i.on_kick(msg))
                if (code == Bytes.b_OnlineState and "on_online_state" in dir(i)):
                    asyncio.ensure_future( i.on_online_state(msg))
                if (code == Bytes.b_PollInit and "on_poll_init" in dir(i)):
                    asyncio.ensure_future( i.on_poll_init(msg))
                if (code == Bytes.b_PollResult and "on_poll_result" in dir(i)):
                    asyncio.ensure_future( i.on_poll_result(msg))
                if (code == Bytes.b_RaffleRun and "on_raffle_run" in dir(i)):
                    asyncio.ensure_future( i.on_raffle_run(msg))
                if (code == Bytes.b_RemoveMessage and "on_remove_message" in dir(i)):
                    asyncio.ensure_future( i.on_remove_message(msg))
                if (code == Bytes.b_ServerMessage and "on_server_message" in dir(i)):
                    asyncio.ensure_future( i.on_server_message(msg))
                if (code == Bytes.b_Unban and "on_unban" in dir(i)):
                    asyncio.ensure_future( i.on_unban(msg))
                if (code == Bytes.b_UserList and "on_user_list" in dir(i)):
                    asyncio.ensure_future( i.on_user_list(msg))
                if (code == Bytes.b_Whisper):
                    if (msg.incomming == True and "on_whisper_received" in dir(i)):
                        asyncio.ensure_future( i.on_whisper_received(msg))
                    else:
                        if ("on_whisper_sent" in dir(i)):
                            asyncio.ensure_future( i.on_whisper_sent(msg))
                if (code == Bytes.b_Reminder and "on_reminder" in dir(i)):
                    asyncio.ensure_future( i.on_reminder(msg))
                if (code == Bytes.b_Timer and "on_timer" in dir(i)):
                    asyncio.ensure_future( i.on_timer(msg))
                if (code == Bytes.b_ChatLevel and "on_chat_level" in dir(i)):
                    asyncio.ensure_future( i.on_chat_level(msg))
                if (code == Bytes.b_UserCount and "on_user_count" in dir(i)):
                    asyncio.ensure_future( i.on_user_count(msg))
                    
                    
            except:
                print("Unexpected plugin error: " + sys.exc_info()[0])
                pass

""