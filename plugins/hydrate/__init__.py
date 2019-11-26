import sys
import asyncio
from src import Bunn as B
import datetime
from datetime import timedelta

started = False
lastCall = datetime.datetime.now()
testCall = None
conversion = "%Y-%m-%d %H:%M:%S.%f"

def init():
    global lastCall
    global started
    global conversion
    
    if (not started):
        f = open("timestamp.txt", "r+")
        hold = f.read()

        if (len(hold) > 10): 
            f.seek(0)
            lastCall = f.readline().rstrip()

            started = True




async def on_command(msg):
    global started
    global lastCall    
    
    try:  
        cmd = msg.message[1:].split(" ")

        if (cmd[0] == "hydrate"):   
            t = open("timestamp.txt", "r+")
            #temp = t.readline().rstrip()  
            
            t.seek(0)
            t.truncate()     
            
            if (started):
                started = False
                await B.send_message("Break reminder is now OFF.")
            elif (not started):          
                started = True
                t.write("{}".format(datetime.datetime.now()))#, str(started)))

                await B.send_message("Break reminder activated! See you in an hour!")
                
            #print("Command status:")
            #print(started)
            
            t.close()
                
    except:
        print("Error in reminder command code")
        print(sys.exc_info())
        
        
  
async def on_online_state(msg):
    ready = ""
    
    try:    
        ready = await check_time()   
            
        if (ready and started):
            await B.send_message("Remember to save, stretch, and hydrate!")
        elif (not started):
            pass
            #print("Reminder not started.")
        else:
            pass
            #print("Reminder not ready. Waiting for next call....")
            
    except:
        print("Error in reminder control code")
        print(sys.exc_info())

        
async def check_time():
    global started
    global lastCall
    global testCall
    global conversion
    #print("Checking time...")
    
    try:    
        #print("Converting time")
        
        if (type(lastCall) is str):
            testCall = datetime.datetime.strptime(lastCall, conversion)
        else:
            testCall = lastCall
            
        #print("Current time:")
        #print(datetime.datetime.now())
        #print("SAVED time:")
        #print(lastCall)
        #print("Entering conditional...")
    
        if (started and (datetime.datetime.now() > (testCall + timedelta(seconds=3600)))):
          
            f = open("timestamp.txt", "w")
            lastCall = datetime.datetime.now()
            testCall = lastCall
            f.write("{}".format(lastCall))#, str(started)))
            f.close()

            print(lastCall)
            #print("Successful reminder")
            return True
        
        else:
            #print("Exited time check")
            return False
    
    except:
        print("Error in reminder time code")
        print(sys.exc_info())
    