# This plugin will automatically remove any message that contains a word
# in our list of swear words.
# The streamer/mods can add/remove words at will.

# These two imports are mandatory
from src import Bunn as B
import asyncio

import os

swears = []
plugin_folder = "./plugins/filter/"
swear_file = "swears.txt"
path = os.path.join(plugin_folder + swear_file)

# Having an init() function is mandatory
# This is called by the plugin manager on startup.
def init():
    file = open(path, 'r')
    lines = file.readlines()
    for i in lines:
        i = i.replace("\n","")
        swears.append(i)
    file.close()

async def on_message(msg):
    message = msg.message
    message = message.lower()
    message = message.replace(' ', '')
    for i in swears:
        if i in message:
            await B.remove_message(msg.id)
            break

'''
Commands:
    !filter
        add
           [word]
        remove
           [word]
        help
           [username]
'''
async def on_command(msg):
    # Lets remove our command character
    message = msg.message[1:]
    # We'll split our message up into ['filter','add'/'remove',<word>]
    message = message.split(' ',2)

    # Permissions for these commands are dictated by the permissions.json file
    if (message[0] == "filter"):
        if (len(message) == 1):
            await whisper_filtered_words(msg.display_name)
        else:
            if (message[1] == "add"):
                await add_swear(message[2])
            if (message[1] == "remove"):
                await remove_swear(message[2])
            if (message[1] == "help"):
                await whisper_help(msg.display_name)

async def add_swear(word):
    global swears
    print(word)
    word = word.replace(' ', '')
    if (word not in swears):
        file = open(path,'a')
        file.write(word+"\n")
        file.close()
        swears.append(word)

async def remove_swear(word):
    global swears
    word = word.replace(' ', '')
    swears_copy = swears.copy()
    swears_copy.remove(word)
    file.open(path,'w')
    for i in swears_copy:
        file.write("{}\n".format(i))
    swears = swears_copy

async def whisper_help(user):
    await B.whisper(user,"FILTER PLUGIN")
    await asyncio.sleep(1)
    await B.whisper(user,"!filter | Displays all filtered words")
    await asyncio.sleep(1)
    await B.whisper(user,"!filter <add/remove> <word> | Adds or removes a given word")
    await asyncio.sleep(1)
    await B.whisper(user,"!filter help | What you're seeing right now, silly!")

async def whisper_filtered_words(user):
    global swears
    for i in swears:
        await B.whisper(user,i)
        await asyncio.sleep(1)
