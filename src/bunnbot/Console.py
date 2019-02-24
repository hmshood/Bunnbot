
import sys
import asyncio
import traceback
from aioconsole import ainput
from concurrent.futures import ThreadPoolExecutor
from src.bunnbot import Client
from src import Bunn as B

_executor = ThreadPoolExecutor(2)

class BunnConsole(object):
    def __init__(self, client, event_loop):
        self.client = client
        self.loop = event_loop
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
              data = await ainput()  
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

    '''
    BunnConsole.show_help
    Args:
        NONE

    Displays the help menu. Shows the possible commands the user can call from the console,
    and displays the copyright and licensing information.

    This function is NOT asynchronous, meaning it must be called using run_in_executor
    '''
    def show_help(self):
        print("")
        print("*"*50)
        print("BunnBot v{}".format(0.1))
        print("BunnBot Source (c) Alexander J. (KingCrazy) 2018")
        print("BunnBot is a free, open source chatbot for the PicartoTV streaming platform.")
        print("If you're paying to download and use this source code, please contact the developer immediately.\n")
        print("Contact information:\nEmail:\tFloppyEarFreak@gmail.com\nGitHub:\tgithub.com/KingCrazy\n")
        print("Items in \"< >\" are required variables.")
        print("Items in \"[ ]\" are optional varaibles.\n")
        self.print_command("SAY <message>", "Prints a given message to the chat.")
        self.print_command("RELOAD [plugin]","Reloads the specified plugin. If no plugin is given, reloads all plugins.")
        self.print_command("QUIT", "Disconnects the bot and closes out the application.")
        self.print_command("HELP", "Displays the help menu... But you knew that already!")
        print("\nSpecial Thanks:\n\tAndrew Silver (PicartoTV)\n\tTheComet (github.com/TheComet)")
        print("*"*50)
        print("")
        return

    '''
    BunnConsole.print_command
    Args:
        (string)    cmd
        (string)    msg

    A fancy way of printing out the commands because I'm lazy and like to make functions for everything.
    '''
    def print_command(self, cmd, msg):
        print("{0:<16}{1}".format(cmd,msg))
