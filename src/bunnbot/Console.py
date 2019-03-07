
import sys
import asyncio
from asynccmd import Cmd
from src import Bunn as B
from src.bunnbot import Client
from concurrent.futures import ThreadPoolExecutor



#from cmd import Cmd

class BunnConsole(Cmd):
  
    def __init__(self, mode, intro, prompt):
        # We need to pass in Cmd class mode of async cmd running
        super().__init__(mode=mode)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_exit(self, args): #override default asynccmd exit
        """Quits the program."""
        print ("Quitting.")
        for i in asyncio.Task.all_tasks():
            i.cancel()
        
    def start(self, loop=None):
        # We pass our loop to Cmd class.
        # If None it try to get default asyncio loop.
        self.loop = loop
        # Create async tasks to run in loop. There is run_loop=false by default
        super().cmdloop(loop)
        


    
    
    
"""
class BunnConsole(object):


    '''
    #BunnConsole.handle_command
    #Args:
    #    (string)    cmd
    #    (string)    data

    #Essentially a big switch statement for running commands from the client.
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


    '''
    #BunnConsole.show_help
    #Args:
    #    NONE

    #Displays the help menu. Shows the possible commands the user can call from the console,
    #and displays the copyright and licensing information.

    #This function is NOT asynchronous, meaning it must be called using run_in_executor
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

"""
