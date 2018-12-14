# Python 3.6
# (c) Alexander J. (KingCrazy) 2018

import imp
import importlib
import os
import asyncio
import sys
import json
from src import Bytes
from src import Consts as C
from src import PermissionAuthority as PA
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(2)

plugin_folder = "./plugins"
main_module = "__init__"
permission_authority = PA.PermissionAuthority()
permissions_file = "permissions.json"
plugin_config_file = "plugins.json"



class PluginManager():
    def __init__(self):
        self.plugins = []
        self.plugin_json_data = {}
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
        self.load_plugin_config()
        for i in plugin_files:
            path = os.path.join(plugin_folder, i)

            if not os.path.isdir(path) or not main_module + ".py" in os.listdir(path):
                continue

            info = importlib.import_module("plugins." +i)
            #print(info.__name__)
            if (self.check_plugin_enabled(info.__name__.split(".")[1])):
                plugins.append(info)
                self.load_permissions(path,False)
                print("Loaded plugin: {}".format(i))
            #info = importlib.machinery.PathFinder().find_spec(main_module, [path])
            #plug = self.load_plugin(info)
            #self.plugins.append(plug)
            #info.loader.exec_module(plug)
            #plugins.append(info)#{"name":i,"info":info})

        self.update_plugin_config()
        return plugins

    def load_plugin_config(self):
        try:
            with open(plugin_config_file,'r') as plugin_config:
                self.plugin_json_data = json.load(plugin_config)
                print("Plugin config loaded")
                return True
            return False
        except FileNotFoundError:
            print("No plugins.json file found. Creating plugins.json")
            with open(plugin_config_file,"w+") as plugin_config:
                plugin_config.write("{}")
                return True
            return False

    def update_plugin_config(self):
        #try:
        with open(plugin_config_file,'w') as plugin_config:
            json.dump(self.plugin_json_data, plugin_config, indent=1)
            print("Plugin config dumped")
        #except Exception:
        #    print("Error writing to plugins.json")

    def check_plugin_enabled(self, plugin_name):
        keys = self.plugin_json_data.keys()
        if (plugin_name in keys):
            val = self.plugin_json_data[plugin_name].lower()
            if (val == "true" or val == "1" or val == "enabled"):
                return True
            else:
                return False
        else:
            print("" + plugin_name + " not found in keys")
            self.plugin_json_data[plugin_name] = "true"
            return True

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
