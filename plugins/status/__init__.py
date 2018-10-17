from src import Bunn as B
from src import Consts as C
import asyncio

import time
import os

filename = "config.txt"
plugin_folder = "./plugins/status/"
file_path = os.path.join(plugin_folder, filename)

active_msg = "Drawing art"
away_msg = "BRB! :heart:"
return_msg = "And we're back!"

timer_length = 120
last_time = 0

active = True
away = False

def init():
    load_config()
    pass

def load_config():
    global active_msg
    global away_msg
    global return_msg
    global timer_length

    if (os.path.exists(file_path)):
        try:
            with open(file_path,'r') as file:
                active_msg = file.readline()
                away_msg = file.readline()
                return_msg = file.readline()
                timer_length = float(file.readline())
        except ValueError:
            print("Error loading status plugin config file. Reloading default config.")
            default_config()
    else:
        print("Error: status plugin config file does not exit. Creating default file.")
        default_config()

def default_config():
    global active_msg
    global away_msg
    global return_msg
    global timer_length

    active_msg = "Drawing art"
    away_msg = "BRB! :heart:"
    return_msg = "And we're back!"
    timer_length = 120

    with open(file_path,'w+') as file:
        file.write("{0}\n{1}\n{2}\n{3}".format(active_msg.strip("\n"),away_msg.strip("\n"),return_msg.strip("\n"),timer_length))

async def on_command(msg):
    cmd = msg.message[1:].split(" ")

    global active_msg
    global away_msg
    global return_msg
    global timer_length
    global away
    global active

    try:
        if (cmd[0] == "currently"):
            if (cmd[1] == "away"):
                cmd = msg.message[1:].split(" ", 2)
                away_msg = cmd[2]
                await update_config()
                await B.send_message("Away message updated.")
                if (away == True):
                    await asyncio.sleep(0.1)
                    await update_status(True,away_msg)
            elif (cmd[1] == "return"):
                cmd = msg.message[1:].split(" ", 2)
                return_msg = cmd[2]
                await update_config()
                await B.send_message("Return message updated.")
            elif (cmd[1] == "timer"):
                cmd = msg.message[1:].split(" ")
                timer_length = float(cmd[2])
                await update_config()
                await B.send_message("Interval changed to {} seconds.".format(timer_length))
            elif (cmd[1] == "stop"):
                active = False
                await B.send_message("I'll no longer notify the chat about your status.")
            elif (cmd[1] == "start"):
                active = True
                if (away == True):
                    await update_status(True,away_msg)
                else:
                    await update_status(False,active_msg)
            else:
                active_msg = msg.message[1:].split(" ", 1)[1]
                await update_config()
                if (away == False):
                    await update_status(False,active_msg)
        elif (cmd[0]=="whatsup"):
            if (away == True):
                await update_status(True,away_msg)
            else:
                await update_status(False,active_msg)
        elif (cmd[0].lower() == "brb"):
            if (away == False):
                await update_status(True,away_msg)
        elif (cmd[0].lower() == "back"):
            if (away == True):
                await update_status(False,return_msg)
    except IndexError:
        pass
    except:
        raise

async def on_update():
    global last_time
    if (active == True):
        if (last_time + timer_length < time.time()):
            last_time = time.time()
            if (away == True):
                await B.send_message("Currently: {}".format(away_msg))
            else:
                await B.send_message("Currently: {}".format(active_msg))

async def update_status(away_status,msg):
    global last_time
    global away

    away = away_status
    last_time = time.time()
    await B.send_message("Currently: {}".format(msg))

async def update_config():
    with open(file_path,'w+') as file:
        file.write("{0}\n{1}\n{2}\n{3}".format(active_msg.strip("\n"),away_msg.strip("\n"),return_msg.strip("\n"),timer_length))
