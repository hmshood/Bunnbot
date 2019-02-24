
import time
import asyncio
from src import Bunn as B
#from src.bunnbot import Client

class Player(self, msg):
    def __init__
        self.name = ""
        self.score = 0
        self.LastGuessTime = 0
        self.isSpy = False

trapWord = ""
currThief = ""
playerList = []    # List of objects. Each object will have: playername, score, lastGuessTime, isSpy
minPlayers = 3
guessCd = 5        # Measuresd in in seconds
theifLimit = 300   # Also measured in seconds
listenTime = 300
minMesages = 20
minLength = 3
guessPenalty = -1  # Points lost to wrong guest over whispers
winPoints = 5


       


def init():
    pass
  

async def on_command(msg):
  # Needed commands: Base, start, end, afk, help
  msg = await sanitize_input(msg)
  cmd = msg.message[1:].split(" ")
  
  
async def on_message(msg):
  
  
  
  
async def sanitize_input(msg):
  try:
    msg.message = parser.unescape(msg.message)
    return msg
  except:
    print("Sanitization error.")
  
  
  
  
'''
1.) Have bot pick a random word that was said in chat (must not be any of the 100 most common words in English and longer than 2 letters)

2.) Bot will signal the game has begun by saying into chat: The (spellbook/safe?) is/are up for grabs! Hurry, get it with: [ !yoink ]

3.) If three or more people input a !yoink in the seconds afterward, the game can begin. Otherwise, there are too few players to play the game.

4.) The bot will say into chat: 

    Someone took the (?)! But who? 
    Whoever it was, they'll try to trick you into saying a specific word! 
    Each time non-theifs say that word, the theif SILENTLY gets a point!
    Once the theif gets X points, they win!
    
    BUT! After X minutes pass OR if anyone correctly guesses the word by typing [ !yoink <YourGuessHere> ], the (?) will be up for grabs again!
    If the thief loses control of the (?), they cannot pick it up until the next time it drops.
    (If you whisper @BotName the correct guess, you'll gain points when the theif does!)
    (If you whisper @BotName a WRONG guess, however, you'll lose a point!)
    
5.) Whenever the (?) is picked back up, the scoreboard updates and it output to chat, but only the scores and placements, not the people who have them.

6.) At the same time, whoever was randomly chosen to get the (?) is whispered by the bot of the trap word (from step 1) and their win condition

7.) Every time they get someone to say the word (or they do it themselves), the bot whispers their score to them.

8.) The only things announced in public are the basic rules and whether or not the (?) is up for grabs. As well as user guesses

'''
