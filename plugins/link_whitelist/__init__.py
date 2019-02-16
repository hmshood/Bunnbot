from src import Bunn as B
from src import Config as C
import asyncio
import os

plugin_folder = "./plugins/link_whitelist"
filename = "whitelist.txt"
path = os.path.join(plugin_folder, filename)
disabled = False
# Our list of whitelisted websites, loaded in at the start.
whitelist = []

# A collection of common domains that we can check, in case the link doesn't have www., http:// or https:// in it.
domains = [".com",".net",".org",".me",".tk",".ca",".us",".uk",".edu",".gov",".ru",".cn",".de",".jp",".es",".info",".eu",".nl",".tv"]

def init():
    load_whitelist()

def load_whitelist():
    if (os.path.exists(path)):
        with open(path,'r') as file:
            lines = file.readlines()
            for i in lines:
                if ("#" not in i):
                    i = i.replace("\n","").replace("http://","").replace("https://","")
                    whitelist.append(i)
    else:
        f = open(path,'w+')
        f.close()

async def on_command(msg):

    global disabled

    # Grab our message, remove the leading command char, and split it up into parts
    message = msg.message[1:].split(" ")

    # Check to see if we're trying to use this plugin
    if (message[0] == "link_whitelist"):

        # We'll wrap this in a try block, just in case the user doesn't put enough
        # parameters with their command.
        try:
            # Here's what we'll do if they try to add a url to the whitelist
            if (message[1] == "add"):
                await add_url_to_whitelist(message[2])
                print("Link Whitelist: url " + message[2] + " added to whitelist")
            # Else, here's what we'll do if they try to remove a url from the whitelist
            elif (message[1] == "remove"):
                await remove_url_from_whitelist(message[2])
                print("Link Whitelist: url " + message[2] + " removed from whitelist")
            elif (message[1] == "disable" and disabled == True):
                disabled = False
            elif (message[1] == "enable" and disabled == False):
                disabled = True
        except:
            pass

async def on_message(msg):
    if (disabled == True):
        return

    message = msg.message

    if (msg.user_id == C.bot_channel_id or msg.streamer == True or msg.moderator == True):
        return

    # We'll make our message all lowercase so it's easier to check for things.
    message = message.lower()

    should_remove = True

    # Let's check to see if someone posted a link
    if "http://" in message or "https://" in message or "www." in message or await check_domain(message):
        # We'll check it with our whitelist
        for i in whitelist:
            # Capitalization doesn't really matter with urls, so we'll just lowercase our whitelist items just in case
            if i.lower() in message:
                # We've found the url in our whitelist. We don't need to do anymore checking
                # since we know the link is clean. We should NOT remove the link,
                # and we should break out of the loop.
                should_remove = False
                break

        # If we never found the link in our whitelist...
        if (should_remove == True):
            await B.remove_message(msg.id)
            await B.send_message("Whoa!! That link looked a little suspiscious! Please refrain from posting links to strange websites!")

async def check_domain(message):
    for i in domains:
        if i in message:
            return True
    return False

async def add_url_to_whitelist(url):
    if (url not in whitelist):
        with open(path,'a') as file:
            file.write(url + "\n")
        whitelist.append(url)

async def remove_url_from_whitelist(url):
    if (url in whitelist):
        whitelist.remove(url)
        with open(path, 'w') as file:
            for i in whitelist:
                file.write(i + "\n")
