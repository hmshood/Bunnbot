# Rolls a dice with a given number of sides.

# TODO: We need some sort of config file to tell us what commands work for what level of people

# These two imports are mandatory
from src import chat_pb2
from src import Bunn as B
import asyncio

# We're importing random, so we can roll dice later!
import random

# init() is mandatory
def init():
    # It's required to have this function, but we'll just pass.
    # We don't need to set up anything ahead of time!
    pass

# This will be called whenever someone enters a command in the chat.
async def on_command(msg):
    # We'll take the message from our msg object (see: definition of chat_pb2.ChatMessage())
    # and we'll grab the text. We'll split off the first character (our command character)
    message = msg.message[1:]

    # ...and then split it up into a list of words, separated at the space.
    message = message.split(" ")

    # if the command starts with roll, we know we need to do something.
    if (message[0] == "roll"):
        # It's always good to initialize your variables ahead of time!
        # For instance, what if setting roll fails later? What would we be
        # sending to the chat?
        roll = -1

        # Whenever you're unsure about something succeeding, always wrap it
        # in a try/catch block! This way, your program won't break if something
        # goes wrong!
        try:
            # Checking to see if the user just typed !roll or !roll <number>
            # Here's what we do if they just typed !roll
            if (len(message) == 1):
                # We'll roll a 6-sided die (random.randint(<min>,<max>) is inclusive)
                roll = random.randint(1,6)
                # We'll then print out the roll's result to the chat
                # msg (see: chat_pb2.ChatMessage()) has a variable "display_name" which
                # is the person who originally called the command.
                await print_roll(msg.display_name,roll)
            # Here's what we do if they typed !roll <number>
            elif (len(message) > 1):
                # We'll roll a <number>-sided die
                # We wrap message[1] around int() in order to turn a string into an integer
                roll = random.randint(1,int(message[1]))
                # We'll then print out the roll's result to the chat
                # msg (see: chat_pb2.ChatMessage()) has a variable "display_name" which
                # is the person who originally called the command.
                await print_roll(msg.display_name,roll)
        except:
            # Oopsies! Something went wrong! We'll just pass over the issue.
            pass

# This function takes in a username and roll and prints it out to the chat.
async def print_roll(username,roll):
    # <str>.format() helps us format strings!
    # {0} will get replaced by the first variable, "username", and {1} will
    # get replaced by the second, "roll"
    # Example result: "KingCrazy rolled a 3!"
    print("Rolling...")
    await B.send_message("{0} rolled a {1}!".format(username, roll))
