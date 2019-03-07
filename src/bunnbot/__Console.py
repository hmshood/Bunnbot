import sys
from asyncio import *
from aioconsole import ainput

_client_sessions = []
_curr_session = None

class BunnConsole(object):
    
    def __init__(self, loop, client = None):
        self.client = client
        self.loop = loop
    '''
    BunnClient.read_console
    Args:
        NONE

    This function handles the input from the console.
    It runs as a separate Task from the listen() function.
    '''
    async def read_console(self):
        try:
            while (True):
                data = await ainput('Input >>>') 
                print(data)
                if not data:
                    break
                else:      
                    cmd = data.split(" ")[0].lower()       
                    data = data.replace(cmd, "", 1).replace(" ", "", 1)    
                    await self.handle_command(cmd,data)  

                await asyncio.sleep(0.1)    
        except:
          print("Oop! Something went wrong with the console.")
          print(sys.exc_info())
          raise

    '''
    BunnConsole.handle_command
    Args:
        (string)    cmd
        (string)    data

    Essentially a big switch statement for running commands from the client.
    '''
    async def handle_command(self,cmd,data):
        if cmd == "quit":
            print("Quitting BunnBot.")
            await self.client.close()
        elif cmd == "users":
            await B.request_user_list()
        elif cmd == "say":
            await B.send_message(data)
        elif cmd == "reload":
            if (len(data)>0):
                # Reload specific plugin
                await self.client.plugin_manager.async_reload_plugin(data)
            else:
                # Reload all
                await self.client.plugin_manager.async_reload_plugins()
        elif cmd == "help":
            try:
                await self.loop.run_in_executor(_executor, self.show_help)
            except:
                print(traceback.print_exc())
                pass