from src import Bunn as B
#from src.protocol import chat_pb2
import asyncio

from src import Config as C
from datetime import datetime, timezone
import requests

is_live = False

def init():
    pass

async def on_online_state(msg):
    global is_live
    is_live = msg.is_live

async def calculate_time(msg_time):
    ctime = await get_last_online()
    ctime = ctime[:len(ctime)-3] + ctime[len(ctime)-2:]

    s = datetime.strptime(ctime, '%Y-%m-%dT%H:%M:%S%z')
    m = datetime.fromtimestamp(msg_time, s.tzinfo)

    return m - s

async def get_last_online():
    req = requests.get(C.api_url + C.api_v + 'channel/name/' + C.channel_name)
    return req.json()['last_live']

async def on_command(msg):
    message = msg.message[1:].split(" ")

    time_str  = ["hours","minutes","seconds"]

    ctime = await calculate_time(msg.time_stamp)

    calc_time = {"hours":0,"minutes":0,"seconds":0}

    calc_time['hours'] = (ctime.seconds // 3600) + (ctime.days * 24)
    calc_time['minutes'] = (ctime.seconds // 60) % 60
    calc_time['seconds'] = ctime.seconds % 60

    if (calc_time['hours'] == 1):
        time_str[0] = "hour"
    if (calc_time['minutes'] == 1):
        time_str[1] = "minute"
    if (calc_time['seconds'] == 1):
        time_str[2] = "second"

    if message[0] == "uptime":
        if (is_live == True):
            await B.send_message("We've been streaming for {0} {1}, {2} {3}, and {4} {5}!".format(calc_time['hours'], time_str[0], calc_time['minutes'], time_str[1], calc_time['seconds'], time_str[2]))
        else:
            await B.send_message("We were last live {0} {1}, {2} {3}, and {4} {5} ago!".format(calc_time['hours'], time_str[0], calc_time['minutes'], time_str[1], calc_time['seconds'], time_str[2]))
