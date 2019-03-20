# Python 3.6
# (c) Alexander J. (KingCrazy) 2018
# BunnClient

import sys
import requests
import asyncio
import websockets
import traceback
import time
import datetime
from src import PluginManager
from src import chat_pb2
from src import Bunn
from src import Bytes
from src import Consts as C
from google.protobuf.message import Message
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from concurrent.futures import ThreadPoolExecutor


class BunnClient(object):
    __instance = None

    def __new(cls):
        if (cls.__instance == None):
            cls.__instance = object.__new__(cls)
            cls.__instance.name = "Client"
        return cls.__instance

    def __init__(self, socket, loop, pm):
        self.websocket = socket
        self.eventloop = loop

        self.cmsgs = {}
        self.user_list = []

        self.is_reminder_set = False
        self.is_timer_set = False

        #self.console = Console.BunnConsole(self, loop)
        self.console = False ###change this later when console decoupled from code

        self.plugin_manager = pm
        self.start_listening_time = 0

    '''
    BunnClient.main
    Args:
        NONE

    This is where it all begins!
    '''
    async def main(self):
        print ("Connected!")
        plugins = asyncio.Task(self.plugin_manager.on_update())
        await asyncio.sleep(0.1)
        #await self.plugin_manager.on_init()
        self.start_listening_time = time.time()
        
        
        
        while (True):
            #data = await self.websocket.recv()
            #print(data[0])
            #print("Loop!")
            await self.listen()
            await asyncio.sleep(0.1)
            
              
            #print("GO!")

    '''
    BunnClient.close
    Args:
        NONE

    Handles closing out of everything.
    This is located in the client, because the client is our hub.
    Also, that way we don't have to pass the websocket around, or awkwardly
    access the websocket from the client from another class.
    '''
    async def close(self):
        for i in asyncio.Task.all_tasks():
            i.cancel()
        self.websocket.close()

    '''
    BunnClient.listen
    Args:
        NONE

    Listen does just that: It listens for the incoming messages from the websocket.
    Picarto's servesr send data in the form of bytes, the first byte of which is a message ID.
    The message ID corresponds to a specific function in the chat.proto file.

    Here is where we parse the message id number, and handle those incoming messages.
    This function does most of the heavy work.
    '''
    async def listen(self):
        try:
            #print ("Task count: " + str(len(asyncio.Task.all_tasks())))
            # Receiving data from the socket...
            data = await self.websocket.recv()
            if (data):

                # We'll grab the first byte from the data... aka our message ID
                message_type_id = data[0]
                await self.print_override("Received message ID: {}".format(data[0]))
                # We snip off the first byte and save the rest of the data for later.
                data = data[1:]
                # ID: 0; Admin Control
                # These are messages sent by the admins of Picarto.
                # Hopefully you'll never need this.
                if (message_type_id == Bytes.b_AdminControl[0]):
                    msg = chat_pb2.AdminControl()
                    msg.ParseFromString(data)
                    await self.print_override("Admin control: " + str(msg.message_type))
                # ID: 1; Ban
                # The message sent by the server when a ban has taken place.
                if (message_type_id == Bytes.b_Ban[0]):
                    msg = chat_pb2.Ban()
                    msg.ParseFromString(data)

                    await self.plugin_manager.on_event(Bytes.b_Ban,msg)

                    if (msg.is_shadow_ban == True):
                        ban_str = "shadow banned"
                    else:
                        ban_str = "banned"
                    await self.print_override("{0} has been {1} by {2}".format(msg.display_name,ban_str,msg.executioner_display_name))
                # ID: 2; Chat Message
                # This is what we do when we read a chat message
                if (message_type_id == Bytes.b_ChatMessage[0]):
                    msg = chat_pb2.ChatMessage()
                    msg.ParseFromString(data)

                    self.cmsgs[msg.id] = msg

                    name = msg.display_name
                    uid = msg.user_id
                    text = msg.message
                    timestamp = msg.time_stamp

                    # We'll only print messages from here on out. We don't want to print messages
                    # that happened before our bot started.
                    # TODO: We also shouldn't care about the Bot's messages.
                    if (timestamp >= self.start_listening_time and uid != C.bot_channel_id):
                        await self.plugin_manager.on_event(Bytes.b_ChatMessage,msg)
                        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        printable = "({0} {1}) {2} | {3} : {4}".format(timestamp,"Local Time",uid,name,text)
                        await self.print_override(printable)
                # ID: 3; Clear History
                # Occurs whenever the history has been cleared.
                if (message_type_id == Bytes.b_ClearHistory[0]):
                    msg = chat_pb2.ClearHistory()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_ClearHistory,msg)
                    await self.print_override("{0} has cleared the history".format(msg.executioner_display_name))
                # ID: 4; Clear User Message
                # Occurs whenever someone clears the messages of a specified user
                if (message_type_id == Bytes.b_ClearUserMessages[0]):
                    msg = chat_pb2.ClearUserMessages()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_ClearUserMessages,msg)
                    await self.print_override("All messages by {0} have been cleared".format(msg.username))
                # ID: 7; Control
                if (message_type_id == Bytes.b_Control[0]):
                    msg = chat_pb2.Control()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_Control,msg)
                    #print(message.message_type)
                # ID: 10; Kick
                # This message occurs when a user has been kicked.
                if (message_type_id == Bytes.b_Kick[0]):
                    msg = chat_pb2.Kick()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_Kick,msg)
                    await self.print_override("User {0} has been kicked by {1}".format(msg.display_name, msg.executioner_display_name))
                # ID: 16; Online State
                # This is called periodically to get the status of the channel we're connected to.
                if (message_type_id == Bytes.b_OnlineState[0]):
                    msg = chat_pb2.OnlineState()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_OnlineState,msg)
                    await self.print_override("Channel status:")
                    await self.print_override("{0} | Is live: {1} | {2} viewer(s)".format(msg.channel_name, msg.is_live, msg.viewers))
                # ID: 17; Poll Init
                # Called when a poll has been initialized. Both a Client->Server and Server->Client call
                if (message_type_id == Bytes.b_PollInit[0]):
                    msg = chat_pb2.PollInit()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_PollInit,msg)
                    await self.print_override("Poll has begun! \"{0}\"\n{1}".format(msg.question,msg.options))
                # ID: 18; Poll Result
                # Called when the poll result is sent
                if (message_type_id == Bytes.b_PollResult[0]):
                    msg = chat_pb2.PollResult()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_PollResult,msg)
                    await self.print_override("Poll has ended!")
                # ID: 23; Raffle Run
                # Called when a raffle is run
                if (message_type_id == Bytes.b_RaffleRun[0]):
                    msg = chat_pb2.RaffleRun()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_RaffleRun,msg)
                    await self.print_override("Raffle has been run! Winner: {0}".format(msg.winner))
                # ID: 24; Remove Message
                # This is called whenever a message is removed.
                if (message_type_id == Bytes.b_RemoveMessage[0]):
                    msg = chat_pb2.RemoveMessage()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_RemoveMessage,msg)
                    await self.print_override("{0} removed message {1}".format(msg.executioner_display_name, msg.id))
                # ID: 25; Server Message
                # Activates whenever a server message is received.
                # Server messages would be like a response for setting a timer, or reminder.
                if (message_type_id == Bytes.b_ServerMessage[0]):
                    msg = chat_pb2.ServerMessage()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_ServerMessage,msg)
                    await self.print_override("Server: {}".format(msg.message))
                # ID: 26; Unban
                # A message that occurs when a user has been unbanned from the chat
                if (message_type_id == Bytes.b_Unban[0]):
                    msg = chat_pb2.UnBan()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_Unban,msg)
                    await self.print_override("{0} has been unbanned by {1}".format(msg.display_name, msg.executioner_display_name))
                # ID: 27; User List
                # Occurs whenever the user list is requested.
                if (message_type_id == Bytes.b_UserList[0]):
                    msg = chat_pb2.UserList()
                    msg.ParseFromString(data)
                    self.user_list = msg.user
                    await self.plugin_manager.on_event(Bytes.b_UserList,msg)
                    #print(self.user_list)
                # ID: 28; Whisper
                # This happens whenever a whisper is received (and sent?)
                if (message_type_id == Bytes.b_Whisper[0]):
                    msg = chat_pb2.Whisper()
                    msg.ParseFromString(data)

                    await self.plugin_manager.on_event(Bytes.b_Whisper,msg)

                    if (msg.incomming == True):
                        timestamp = datetime.datetime.fromtimestamp(msg.time_stamp).strftime('%Y-%m-%d %H:%M:%S')
                        await self.print_override("({0} {1}) [PSSST!] {2}: {3}".format(timestamp, "Local Time", msg.display_name, msg.message))
                # ID: 30; Name Confirmation
                # Kind of pointless, but we'll relay a message just in case we need it.
                if (message_type_id == Bytes.b_NameConfirmation[0]):
                    msg = chat_pb2.NameConfirmation()
                    msg.ParseFromString(data)
                    await self.print_override("Name Confirmation response: " + msg.response)
                # ID: 33; Reminder
                # Fires off whenever a reminder notification arrives.
                if (message_type_id == Bytes.b_Reminder[0]):
                    msg = chat_pb2.Reminder()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_Reminder,msg)
                    await self.print_override("Reminder: {}".format(msg.message))
                # ID: 34; Timer
                # Fires off whenever a timer notification arrives
                if (message_type_id == Bytes.b_Timer[0]):
                    msg = chat_pb2.Timer()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_Timer,msg)
                    await self.print_override("Timer: {}".format(msg.message))
                # ID: 36; Chat Level
                # This just tells us the chat level of our room
                if (message_type_id == Bytes.b_ChatLevel[0]):
                    msg = chat_pb2.ChatLevel()
                    msg.ParseFromString(data)
                    await self.plugin_manager.on_event(Bytes.b_ChatLevel, msg)
                    clvl = msg.chat_level
                    if clvl == 0:
                         await self.print_override("Chat level: Everyone")
                    elif clvl == 1:
                        await self.print_override("Chat level: Streamer Only")
                    elif clvl == 2:
                        await self.print_override("Chat level: Moderator")
                    elif clvl == 3:
                        await self.print_override("Chat level: Moderator & Subscriber")
                    elif clvl == 4:
                        await self.print_override("Chat level: Moderator & Follower")
                    elif clvl == 5:
                        await self.print_override("Chat level: Moderator & Subscriber & Follower")
                    elif clvl == 6:
                        await self.print_override("Chat level: Registered Members")
                    else:
                        await self.print_override("Chat level: {}".format(clvl))
                # ID: 39; User Count
                # Is called whenever the user count is updated (user enters/exits)
                if (message_type_id == Bytes.b_UserCount[0]):
                    msg = chat_pb2.UserCount()
                    msg.ParseFromString(data)
                    # We'll update our user list appropriately.
                    await Bunn.request_user_list()
                    await self.plugin_manager.on_event(Bytes.b_UserCount, msg)
                # ID: 44; Ping Pong
                # I've been informed that OCCASIONALLY the server will call PingPong to a client, and will
                # expect a reply. I've tried to cover both bases, but I've never had it do this so it needs
                # testing.
                if (message_type_id == Bytes.b_PingPong[0]):
                    msg = ret = chat_pb2.PingPong()
                    msg.ParseFromString(data)
                    if msg.type == 0:
                        ret.type = 1
                    else:
                        ret.type = 0
                    await self.send_data(msg,Bytes.b_PingPong)
            else:
                print("Closing.")
        except:
            raise


    '''
    BunnClient.get_message_from_id
    Args:
        (int)   message_id
    Returns:
        ChatMessage : Success
        NONE        : Failure

    Searches though a copy of the list of chat messages stored in cmsgs
    in order to retrieve a specified message from the given message_id.
    '''
    def get_message_from_id(self, message_id):
        cmsgs_copy = self.cmsgs.copy()
        for i in cmsgs_copy:
            if cmsgs_copy[i].id == message_id:
                return cmsgs_copy[i]
        return None

    '''
    BunnClient.get_user_from_username
    Args:
        (string)    username (optional*)
        (int)       uid (optional*)

    * One or more of these must be assigned. They can't both be equal to None.

    Returns:
        UserList.User   : Success
        NONE            : Failure

    Retrieves a user object from the list of users
    '''
    def get_user(self, username=None, uid=None):
        print(len(self.user_list))
        if (len(self.user_list) == 0):
            print("User list is empty.")
            return None

        if (username == None and uid == None):
            print("Can't get user without username or user ID")
            return None
        else:
            user_list_copy = self.user_list.copy()
            for i in user_list_copy:
                if (user_list_copy[i].display_name == username or user_list_copy[i].user_id == uid):
                    return user_list_copy[i]
        return None

    '''
    Derecated: use clear_user instead
    '''
    async def clear_user_messages(self, username=None, uid=None):
        if (username == None and uid == None):
            print("Please provide a username or user ID to clear the messages of")
            return
        else:
            for i in self.cmsgs:
                if (self.cmsgs[i] != None):
                    if (self.cmsgs[i].display_name == username or self.cmsgs[i].user_id == uid):
                        await self.remove_message(self.cmsgs[i].id)

    '''
    BunnClient.send_data
    Args:
        (message)   message
        (byte)      byte

    This is where most of the communication boils down to. This function
    takes in a message object that Picarto will recognize, defined in chat_pb2,
    and the byte of data we need to tell Picarto what kind of message we're sending
    (valid bytes are defined in src.Bytes, beginning with "Bytes.b_").

    We serialize the message we want to send (so the server will understand it),
    and we put the byte, our message ID, on the front of it to tell it what
    we're sending.

    Then, we send it off through the websocket.

    Else, if we can't do that, we'll throw an error.
    '''
    async def send_data(self, message, byte):
        try:
            data = message.SerializeToString()
            data = byte+data
            await self.websocket.send(data)
        except:
            print("Error sending data.")
            print(sys.exc_info()[0])

    async def print_override(self, text):
        if (self.console):
            print(text)