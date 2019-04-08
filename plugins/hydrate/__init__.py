from src import Bunn as B
#from src.bunnbot import Client
import asyncio

started = False

def init():
    pass

async def on_command(msg):
    global started
    
  
    cmd = msg.message[1:].split(" ")
    
    if (cmd[0] == "hydrate"):    
      if (started):
          started = False
          await B.send_message("Break reminder is now OFF.")
      else:
          started = True
          await B.send_picarto_command("/reminder 1h")
          await B.send_message("Break reminder activated! See you in an hour!")
  
  
async def on_reminder(msg):
    try:
        global started

        if(started):      
            await B.send_message("Remember to save, stretch, and hydrate!")
    except:
        print("Error in reminder")
    
    
