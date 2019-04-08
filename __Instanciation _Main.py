#!/bin/sh
# Python 3.6
# (c) Alexander J. (KingCrazy) 2018
# main

import sys

import requests
import asyncio
import websockets
import traceback
import time
import threading
from src import PluginManager
from src import ConfigManager
from src.bunnbot import Client
from src.bunnbot import Console
from src import Bunn as B
from src import Consts as C
from google.protobuf.message import Message
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from concurrent.futures import ThreadPoolExecutor

client_instances = {}
user_info = []

_executor = ThreadPoolExecutor(2)
_loop = asyncio.get_event_loop()
_plugin_manager = PluginManager.PluginManager()
#<class 'websockets.exceptions.ConnectionClosed'>, ConnectionClosed('WebSocket connection is closed: code = 1001 (going away), no reason',), <traceback object at 0x7fa8ab45cf88>)

'''
start
Args:
    (string?)   channel_id
    (string?)   bot_channel_id

This function retrieves the JWT Key for the provided user, then uses it to connect to
the Picarto websocket server.

After it's connected, we create a Client object and initiates its main() function.
From there, the rest of the work is done by the Client object.
'''
async def start():
    global client_instances
    global user_info
    print ("Authenticating to Picarto servers . . .")
    
    try:
        req = requests.get(C.api_url + C.api_v + 'user/jwtkey', headers={'Authorization': 'Bearer {}'.format(C.access_token)}, params={'channel_id':C.bot_channel_name, 'bot':'true'})
        token = req.text
        
        print("Authentication successful: JWT Key successfully generated")
        print("Connecting to websockets . . .")
    except:
        print("Bot failed in retrieving token.")
        return


    #NOTE: create exception case where bot does not connect if the user in in a multistream (check for multi, then check for subsriber list, then skip connecting if they're in the same room)
    
    with open("users.txt") as f: #Need to actually READ the names to do this shenanigans. Also, put the bot on the top of the list.  
        for line in f:
            name = f.read()
            user_info.append(name)
                
        f.close()  
        for x in range(len(user_info)):
            if (get_channel_id_from_name(user_info[x])):
                  req = requests.get(C.api_url + C.api_v + 'user/jwtkey', headers={'Authorization': 'Bearer {}'.format(C.access_token)}, params={'channel_id':line, 'bot':'false'})
                  token = req.text

                  async with websockets.connect(C.socket_url.format(token)) as websocket:
                      # Creating our Client object.
                      client = Client.BunnClient(websocket, _loop,_plugin_manager)
                      B._client = client
                      client_instances[line] = client
                      user_info[line] = token

        with ThreadPoolExecutor(len(client_instances)) as e:
            task = None
            for client in client_instances:
                task = e.submit(client.main())
                with suppress (asyncio.CancelledError):
                    try:
                        await task
                    except:
                        print("Unhandled exception awaiting bot TASK")
                        print(sys.exc_info())


'''
get_channel_id_from_name
Args:
    (string)    cname
Returns:
    string  : Success
    None    : Failure

Gets a channel's ID from a given channel name. Uses the requests library to call a
GET request to Picarto's servers. If the code returned is 200, then we've succeeded.
Otherwise, we've failed and we'll return None.
'''
def get_channel_id_from_name(cname):
    req = requests.get(C.api_url + C.api_v + 'channel/name/' + cname)
    code = req.status_code
    if code == 200:
        return True
    elif code == 400:
        print("*** Error ***")
        print("Code: 400\nBad request")
    elif code == 403:
        print("*** Error ***")
        print("Code: 403\nYou do not have access to this channel with your access token.")
    elif code == 404:
        print ("*** Error ***")
        print("Code: 404\nThe channel {} does not exist.".format(cname))
    else:
        print("*** Error ***")
        print("Code: {}".format(code))
    ###return None

'''
main
Args:
    NONE

The entry point for the program.
This function retrieves the channel ID, and passes it to start() if successful.
Otherwise, we'll close out immediately.

Start is called asynchronously by our _loop if we successfully have retrieved the channel ID
'''
def main():
    # Load information from our config.ini file
    ConfigManager.load_configuration()
       
    while (True):
        try:
            _loop.run_until_complete(start())
        except (ConnectionResetError, ConnectionClosed):
            print("Connection error.")
            print(sys.exc_info())
            print("Restarting...")

            continue
        except:
            print("Connection Terminated?")
            print(sys.exc_info())
            break

# And so it begins...
main()
