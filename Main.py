# Python 3.6
# (c) Alexander J. (KingCrazy) 2018
# main

import sys

import requests
import asyncio
import websockets
import traceback
import time
from src import PluginManager
from src import ConfigManager
from src import Client
from src import Bunn as B
from src import Config as C
from google.protobuf.message import Message
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from concurrent.futures import ThreadPoolExecutor

_loop = asyncio.get_event_loop()
_plugin_manager = PluginManager.PluginManager()



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
    print ("Authenticating to Picarto servers . . .")

    # Retrieve the JWT Key from the Picarto servers.
    # api_url, api_v, and header are all defined prior.
    # The prior two are for ease of access, in case Picarto changes their API urls.
    # The latter one is because it'd look super ugly to have it right here.
    req = requests.get(C.api_url + C.api_v + 'user/jwtkey', headers={'Authorization': 'Bearer {}'.format(C.access_token)}, params={'channel_id':C.channel_id, 'bot':'true'})
    code = req.status_code
    token = req.text

    # Handle any status code errors we may have gotten from the GET request
    # We'll simply just return out of the function and end the program if we encounter anything
    if code == 400:
        print("*** Error ***")
        print("Code: 400\nBad request")
        return
    elif code == 403:
        print("*** Error ***")
        print("Code: 403\nApplication not authorized to generate a JWT token for this user.")
        return
    elif code == 404:
        print ("*** Error ***")
        print("Code: 404\nThe channel {} does not exist.".format(cname))
        return

    print("Authentication successful: JWT Key successfully generated")
    print("Connecting to websocket . . .")

    # We'll start up our async connection using the Websockets API.
    # We create a websocket connection, "websocket", and pass that to the Client object
    # when we create it.
    # We also pass in a reference to our _loop, which is currently unnecessary (I think), but
    # might be necessary later on down the line.
    async with websockets.connect(C.socket_url.format(token)) as websocket:
        # Creating our Client object.
        client = Client.BunnClient(websocket, _loop,_plugin_manager)
        B._client = client
        #asyncio.ensure_future(client.main())
        # Create our task
        task = asyncio.Task(client.main())
        #task.cancel()
        with suppress (asyncio.CancelledError):
            # We await our task. So basically, we're stopping here for now while Client does the rest.
            await task

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
        return req.json()['user_id']
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
    return None

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

    # We'll give it a good 10 tries to see if we can get the channel ID
    for i in range(10):
        if C.channel_id == '':
            print("Retrieving channel ID . . . Attempt {}".format(i+1))
            C.channel_id = get_channel_id_from_name(C.channel_name)
            print("Retrieving bot channel ID . . .")
            C.bot_channel_id = get_channel_id_from_name(C.bot_channel_name)
        else:
            break

    # If the ID is empty after we go through that, we'll just quit out
    # Otherwise, we'll move on to trying to authenticate
    if C.channel_id == '':
        print ("Could not retrieve channel ID. Check to make sure the username provided is correct.")
        print("Quitting...")
    else:
        print("Channel ID successfully retreived.")
        #asyncio.get_event_loop().set_debug(True)
        _loop.run_until_complete(start())

# And so it begins...
main()
