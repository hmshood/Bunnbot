
import sys
import asyncio
from asynccmd import Cmd
from src import Bunn as B
from src.bunnbot import Client
from concurrent.futures import ThreadPoolExecutor

import functools

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

        for i in asyncio.Task.all_tasks(self.loop):
            print(i)
            i.cancel()
        raise KeyboardInterrupt
        
    def start(self, loop=None):
        # We pass our loop to Cmd class.
        # If None it try to get default asyncio loop.
        self.loop = loop
        # Create async tasks to run in loop. There is run_loop=false by default
        super().cmdloop(loop)
