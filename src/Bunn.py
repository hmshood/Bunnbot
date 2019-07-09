# Python 3.6
# This is the bunn API. These functions are for public use by plugins and other classes.

from src import chat_pb2
from src import Bytes
from src import Consts as C
from src.bunnbot import Client
import asyncio

_client = None


# Thanks to TomFaulkner on Github for This
import threading



'''
request_user_list
Args:
    NONE

Sends a request to the server to return a list of users.
The list of users will be picked up by the listen() function.
'''
async def request_user_list():
    msg = chat_pb2.RequestUserlist()
    await _client.send_data(msg, Bytes.b_RequestUserList)

'''
send_picarto_command
Args:
    (string)    cmd
    (string)    args

Sends a message to the chat in the form of "cmd args".
This function allows us to use Picarto's user commands as a bot.
'''
async def send_picarto_command(cmd, args=None):
    await send_message("{0} {1}".format(cmd,args))

'''
mod
Args:
    (string)    username

Grants mod status to the specified user.
'''
async def mod(username):
    await send_picarto_command("/mod",username)

'''
unmod
Args:
    (string)    username

Removes mod status from the specified user.
'''
async def unmod(username):
    await send_picarto_command("/unmod",username)

'''
timer
Args
    (string)    time_str

Sets a timer for the bot, or removes one if one is already set.
Also sets is_timer_set respectively.

timer_str should be formatted as:
    #h#m#s
Example:
    3h2m5s
The bot will receive a message when the timer is up.
'''
async def timer(time_str=None):
    if (self.is_timer_set == False):
        if (time_str == None):
            print("Unable to set timer: duration not given")
            return
        else:
            self.is_timer_set = True
            await send_picarto_command("/timer", time_str)
    else:
        self.is_timer_set = False
        await send_picarto_command("/timer")

'''
clear_user
Args:
    (string)    username

Clears all messages from the specified user.
'''
async def clear_user(username):
    await send_picarto_command("/clearuser", username)

'''
clear_history
Args:
    NONE

Clears the chat history.
'''
async def clear_history():
    await send_picarto_command("/clear")

'''
ban
Args:
    (string)    username
    (bool)      shadowban

Bans the specified users.
If shadowban is true, it calls the /shadowban command instead.
'''
async def ban(username,shadowban):
    if (shadowban):
        await send_picarto_command("/shadowban", username)
    else:
        await send_picarto_command("/ban", username)

'''
unban
Args:
    (string)    username

Unbans the specified user.
'''
async def unban(username):
    await send_picarto_command("/unban", username)

'''
kick
Args:
    (string)    username

Kicks the specified user from the channel.
'''
async def kick(username):
    await send_picarto_command("/kick", username)

'''
ignore
Args:
    (string)     username

Sets the specified user to ignore.
Unsure if this is just for the bot, or for the channel.
'''
async def ignore(username):
    await send_picarto_command("/ignore", username)

'''
unignore
Args:
    (string)     username

Unignores the specified user.
Unsure if this is just for the bot, or for the channel.
'''
async def unignore(username):
    await send_picarto_command("/unignore", username)

'''
show_mods
Args:
    NONE

Requests a list of mods for/on the channel from the Picarto servers.
The response will be captured in the listen() function
'''
async def show_mods():
    await send_picarto_command("/showmods")

'''
reminder
Args:
    (string)    time_str (optional)
    (string)    message (optional)

Sets or removes a /reminder for the bot.Reminders only notify the user who set them.
The rest of the stream will not be notified when the reminder goes off

Sets is_reminder_set accordingly.

Reminders can only be set once. Be careful when using this, otherwise you may overwrite
a previously set reminder!
'''
async def reminder(time_str=None, message=None):
    if (self.is_reminder_set == False):
        if (time_str == None):
            print("Unable to set reminder: duration was not given")
            return
        else:
            self.is_reminder_set = True
            await send_picarto_command("/reminder", "{0} {1}".format(time_str, message))
    else:
        self.is_reminder_set = False
        await send_picarto_command("/reminder")

'''
whisper

Arguments:
    (string)    username
    (string)    message

Sends a /whisper to the given user with the specified message
'''
async def whisper(username, message):
    await send_picarto_command("/whisper","{0} {1}".format(username, message))

'''
end_poll
Args:
    NONE

Ends a currently running poll.
'''
async def end_poll():
    msg = chat_pb2.PollEnd()
    await _client.send_data(msg,Bytes.b_PollEnd)

'''
poll_init
Args:
    (string)    question
    (string[])  options

Starts a poll with the passed in question and list of options.
'''
async def poll_init(question,options):
    msg = chat_pb2.PollInit()
    msg.question = question
    msg.options = options
    await _client.send_data(msg,Bytes.b_PollInit)

'''
raffle_init
Args:
    (string[])    names

Starts a raffle which incorporates the passed in list of names.
'''
async def raffle_init(names):
    msg = chat_pb2.RaffleInit()
    ###print("-----")
    print(msg.names)
    print(names)
    ###print("<><><>")
    #msg.names = names
    msg.names.extend(names)
    await _client.send_data(msg,Bytes.b_RaffleInit)


'''
remove_message
Args:
    (int)   message_id

Sends a call to the server to remove a specific message from the chat, indicated
by the message_id.
'''
async def remove_message(message_id):
    msg = chat_pb2.RemoveMessage()
    msg.id = message_id
    msg.executioner_id = C.bot_channel_id
    msg.executioner_display_name = C.bot_channel_name
    await _client.send_data(msg, Bytes.b_RemoveMessage)

'''
send_message
Args:
    (string)    message

Sends a regular message to the chat as the bot.
'''
async def send_message(message):
    msg = chat_pb2.NewMessage()
    msg.message = message
    await asyncio.sleep(0.2)
    await _client.send_data(msg, Bytes.b_NewMessage)
