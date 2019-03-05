from cmd import Cmd
import sys

_client_sessions = []
_session = None

class BunnConsole(object):
    
    def __init__(self):
        pass
      
      
    async def start_console(self):
        console = Commander()
        console.prompt = "<><>"
        console.cmdloop()
        
    async def new_session(self):



class Commander(Cmd):
    def do_sessions (self, index):
        if (index):
            print("Whatever witchcraft connects to a session.")
        else:
            print("Client synching witchcraft.")
        
       
    def do_EOF (self, line):
        return True  
        
