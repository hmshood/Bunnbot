
import time
import random  # Need it to choose players
import asyncio
from src import Bunn as B
#from src.bunnbot import Client

class Player(self, msg):
    def __init__
        self.name = ""
        self.score = 0
        self.LastGuessTime = 0
        self.numMistakes = 0
        self.isSpy = False

trapWord = ""
currThief = ""
playerList = []    # List of objects. Each object will have: playername, score, lastGuessTime, pentalty time, isSpy
isGameGoing = False
isForGrabs = False # If the theif object has been taken
minPlayers = 3
guessCd = 5        # Measuresd in in seconds
theifLimit = 300   # Also measured in seconds
listenTime = 100
minMesages = 20
minLength = 3
guessPenalty = -1  # Points lost to wrong guest over whispers
guessReward = 1    # Points gained per right guess of the trap word
winScore = 5

       
def init():
    pass
  

async def on_command(msg):
  # Needed commands: Base, start, end, afk, help
  msg = await sanitize_input(msg)
  cmd = msg.message[1:].split(" ")
  
  if (cmd[0] == "blab"):
      try:
          if (len(cmd == 1):
              
              
          elif (len(cmd[1] > 1):
                
              if (cmd[1] == "start"):           

                  if (not trapWord):
                      print("No trap word detected, gotta make one.")
                      #Use word picking function

                  if (not playerList and not isGameGoing):
                      print("Time to if nerds wanna play. Populate players.")
                      await asyncio.sleep(15)
                      #Hopefully enough players joined by the end of 15 seconds

                  if (len(playerList) < minPlayers and not isGameGoing):
                      print("Too few players to begin. Stopping game.")
                  else:
                      isGameGoing = True
                      isUpForGrabs = True
                      await B.send_picarto_command("/reminder " + thiefLimit +"s")
          
                
              elif (cmd[1] == "end"):                  
                  if (isGameGoing):
                      sGameGoing = False
                      isUpForGrabs = False
                      playerList = []
                      trapWord = ""
                      currThief = ""
                      await B.send_picarto_command("/re")
                      await asyncio.sleep(1)
                      await B.send_message("The {} minigame has now ended! Game state restored to default.".format(cmd[0].title()))
                
                  elif (not isGameGoing):
                      await B.send_message("There are no active games to end!")                
                  else:
                      print("Unexpected game state!")
                
                
              elif (cmd[1] == "help"):
                      print("Tutorial text for players who want to know how to play.")

              
              elif (cmd[1] == "guess"):
                  if (len(cmd) == 3):
                      if (cmd[2] == trapWord):
                          await B.send_message("@{} has correctly identified the word!".format(msg.display_name))
                          await asyncio.sleep(1)
                          await modify_score(msg.displayname, guessReward)
                  elif (len(cmd) > 3):
                      B.send_message("Too many inputs! The guess must be a single word; no spaces!")
                      
      except:
          print("Error in Blab minigame.")
          print(sys.exc_info())
          pass  
      
#############
  
async def on_message(msg):
    pass
 
##############            
          
async def on_reminder(msg):
  try:
      global isGameGoing

      if(isGameGoing):
          await asyncio.sleep(1)
          await B.send_message("Times up for the thief!")
          await disarm_thief()
      else:
          await B.send_picarto_command("/re")  #Cancels reminder cycle
                
  except:
      print("Error in reminder")
                      
##############
                
async def disarm_thief(users):
    pass
#############
                
async def display_standings():
    standings = []
    highest = winScore * -1000
    lowest = winscore * 1000
    buffer = ""          
                
    for user in playerList:
        if (user.score == 0):
            continue
                
        if (user.score > highest):
            highest = user.score
            standings.insert(0, user)
        elif (user.score == highest):
            standings.insert(1, user)
        
        if (user.score <= lowest):
            lowest = user.score
            standings.append(user)
                
        for x in range(len(standings)):
            if (user.score < standings[x].score):
                continue
            standings.insert(x + 1, user)
    
    await B.send_message("Here are the placings!")
    await asyncio.sleep(1)
                
    buffer = "At {} point(s), ".format(standings[0])
                         
    if (len(standings) == 0):               
        await B.send_message("Currently there are no users above 0 points!")
    elif (standings[0].score == standings[1].score and standings[1].score == standings[2].score):
        buffer += "there are THREE players currently TIED for First Place!"
    elif(standings[0].score == standings[1].score and.score standings[1] > standings[2]):
        buffer += "TWO players are TIED in First Place, with ONE player in Second Place with {} point(s)!".format(standings[2].score)
    elif(standings[0].score > standings[1].score and standings[1].score == standings[2].score):
        buffer += "ONE player is in First Place, with TWO people tied for Second Place with {} points(s)!".format(standings[2].score)
    elif: (standings[0].score > standings[1].score and standings[1].score > standings[2].score):
        buffer += "there is ONE player in Frst Place, with Second Place at {0} point(s), and Third Place at {1} point(s)!".format(standings[0].score, standings[1].score, standings[2].score)            
    else:
        buffer = "Something went wrong in scoring! Make sure to tell the nerd who wrote this about this issue!"
                
    await B.send_message(buffer)
                
##############


async def find_player(name):
    for player in playerList:
        if (name == player.username):
            return player
    return 0                
                
##############
                
async def modify_score (user, num, isWhisper = False):
    user = await find_player(user)                
    if (user):
        user.score += num
        await B.send_message("{0} has recieved {1} point(s)!".format(user, num))
    elif (not user):
        await B.send_message("Oh! This player, {}, seems to be missing!".format(user))
                
###############
  
async def sanitize_input(msg, lower = False):
  try:                
    msg.message = parser.unescape(msg.message)
                
    if (lower):
        msg.message = msg.message.lower()
                
    return msg
                
  except:
    print("Sanitization error.")
  
'''

    if (cmd[0].lower() == "gatcha"):
        try:
            if (len(cmd) == 1):     
                    
            elif (len(cmd) > 1):

                if (len(cmd) > 2):   
                       
                      
                elif (smallCmd == "reset"):
                  
                elif (smallCmd == "list"):
                     
                     
                elif (smallCmd == "spin"):                  
                    if (len(users) > 1):         
                                      
                else:
                    await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0].lower()))
                                                                  
        except:
            print("Error in gatcha.")
            print(sys.exc_info())
            pass

'''
  
  
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
