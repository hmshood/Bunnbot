import sys
import asyncio
from src import Bunn as B
import html.parser as htmlparser

parser = htmlparser.HTMLParser()  # Used to keep non-alphanumeric characters in output reable and not an encoded mess.
users = []      
keyDefault = "???"                # This is the default key phrase used to enter the raffle once it's open. DO NOT CHANGE AT PLUGIN RUNTIME
keyPhrase = keyDefault            # The ACTUAL key phrase that'll be used to compare to entrants' input
active = False                    # True = raffle open for key phase entires. False = no more entrants accepted unless force added via coroutine.

def init():                       # There's nothing to setup, but this is required for the plugin to run and, as such, must be declared.
  pass


'''
Commands:
    !gatcha 
        "":               With no command, gatcha outputs if the raffle is open or not; outputting the key phrase if it is.

        open:             Allows entrants to say the case-insensitive, placement-agnostic, key phrase to enter the raffle.

        close:            Blocks any attempt to enter the raffle via key phrase. Does NOT erase the list of entrants or key phrase.

        phrase "":        With no parameters, outputs whether or not the key phrase is set; outputting the key phrase if it is.

        phrase <string>:  Accepts an arbitrary string of characters to set as the key phrase. 
                          Words can be seperated by spaces and will still be considered as part of the phrase. 
                          However, adding more than one space between any word is ineffective and will be concatinated.

        list:             Outputs the number of entrants in the raffle, as well as their usernames in the order of entry. 

        add <?><name>:    Inserts the input user into the raffle, regardless of the key phrase or if the raffle is closed. 
                          The <?> should be an @ symbol if the named user is currently in chat. Otherwise, use # instead.
                          With #, you can insert dummy entrants into the raffle for any reason, and they can be named anything
                          so long as it is one continuous word.
                          
        remove <name>:
                         
        reset:            Sets the key phrase back to its default value and wipes the list of raffle entrants. 
                          Does NOT automatically close the raffle, but a lack of a key phrase will effectively
                          do the same in preventing more entrants.

        spin:             Passes the list of raffle entrants to Picarto's API, using its native raffle function and displaying
                          the winner as per usual. Does NOT automatically clear the entrants list, allowing for additional spins
                          with the same list of people.
                          
        redo:
        
        blacklist +/- <name>:
        
        help:
        
'''


async def on_message(msg):
  global keyPhrase
  msg = await sanitize_input(msg)
  
  #print(msg.message)

    
  if (active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1 and msg.message[0] != "!" and not msg.streamer):
      await addToRaffle(msg, False)
  elif (not active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1):
      await B.send_message("No open raffle to join yet!")      

      
async def on_raffle_run(msg):
    await asyncio.sleep(10)
    await B.send_message(":tada: Congrats, @{} you've won the raffle! :tada:".format(msg.winner))
  
  
  
async def on_command(msg):
    global users
    global active
    global keyPhrase
  
    msg = await sanitize_input(msg)
    cmd = msg.message[1:].split(" ")
      

    if (cmd[0].lower() == "gatcha"):
        try:
            if (len(cmd) == 1):              
                if (active and keyPhrase != "???"):
                    await output_phrase()
                elif (active and keyPhrase == "???"):
                    await B.send_message("Oops! There's a raffle open, but there's no key phrase set! Kindly ask your host to set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                else:
                    await B.send_message("There are no raffles open at this time.")
                    
                    
            elif (len(cmd) > 1):
                smallCmd = cmd[1].lower()
                #print(smallCmd)
              
                if (smallCmd == "open"):
                    if (not active):
                        active = True
                        await B.send_message("Okay, guys! Get ready! The raffle's about to open again!")

                    if (keyPhrase == "???"):
                        await asyncio.sleep(1)
                        await B.send_message("Oh! Well. The raffle is open, but remember to set the key phrase using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                    elif (keyPhrase != "???"):
                        await output_phrase()
                    else:
                        active = False
                        await B.send_message("Error in raffle state ({})! Closing raffle...".format(active))   
                      
                      
                elif (smallCmd == "close"):
                    if (active):
                        active = False
                        #keyPhrase = "???"
                        await B.send_message("The raffle is now closed!")
                    elif (not active):
                        await B.send_message("There are no open raffles to close!")
                    else:
                        await B.send_message("Error in raffle state ({})! Closing raffle...".format(active)) 

                      
                elif (smallCmd == "phrase"):
                    if (len(cmd) > 2):   
                        extraCmd = cmd[2:]
                        extraCmd = " ".join(extraCmd)

                        if (extraCmd != "???"):
                            keyPhrase = extraCmd
                            await B.send_message("NEW KEY PHRASE successfully registered!")
                            await output_phrase()
                        if (extraCmd == "???"):
                            await B.send_message("Sorry, the default value isn't a valid key phrase.")
                       
                    elif (len(cmd) == 2):
                        if (keyPhrase != "???"):
                            await output_phrase()
                        elif (keyPhrase == "???"):
                            await B.send_message("There is no key phrase at this time. Please set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))                  
                        else:
                            print("Unexpected value for key phrase: {}".format(keyPhrase))                              
                      
                      
                elif (smallCmd == "reset"):
                    buffer = ""

                    if (len(users) > 0):
                        users = []
                        buffer = "The list of raffle entrants has been reset "
                    else:
                        buffer = "The current list of raffle entrants is already empty "                    

                    if (keyPhrase != "???"):
                      keyPhrase = "???"
                      buffer += " AND its key phrase has been reset!"
                    elif (keyPhrase == "???"):
                      buffer += " BUT the key phrase remains blank."
                  
                    await B.send_message(buffer)
                  
                  
                elif (smallCmd == "list"):
                      if (len(users) > 0):
                          buffer = "[Current Raffle Entrants ({})]:".format(len(users))
                        
                          for nerds in users:
                              buffer += " {} ,".format(nerds)
                          buffer = buffer.strip(",")
                          await B.send_message(buffer)
                          print(users)

                      else:
                          await B.send_message("There are no entrants to list.")

                          
                elif (smallCmd == "add"):
                    if (len(cmd) == 3 and (cmd[2].startswith("@") or cmd[2].startswith("#"))):
                        await addToRaffle(cmd, True, msg)     # Format: (Prased command split into pieces, Is forced, Raw message object)               
                    else:
                        await B.send_message("Improper input! Please try again using: '{0} {1} @<username>' for named entrants or '{0} {1} #<name>' for anonymous ones!".format(cmd[0], cmd[1]))
                
                
                elif (smallCmd == "remove"):
                    if (len(cmd) == 3):
                        await removeFromRaffle(cmd[2].title())
                    else:
                        await B.send_message("Improper input! Try again using the format of: '{0} {1} username'!".format(cmd[0], cmd[1]))
                
                
                elif (smallCmd == "leave"):
                      await removeFromRaffle(msg.display_name.title())
                  
                  
                elif (smallCmd == "spin"):
                    #print(users)
                  
                    if (len(users) > 1):                       
                        await B.send_message("Raffle spinning! Good luck, guys!")
                        
                        #sendToSpin = " ".join(users)
                        print(users)
                        await asyncio.sleep(3)
                        await B.raffle_init(users)

                    elif (len(users) <= 1):
                        await B.send_message("Sorry, but there aren't enough users for a raffle! You need at least 2 people!")
                
                else:
                    await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0].lower()))
                    
                
                                             
                                             
        except:
            print("Error in gatcha.")
            print(sys.exc_info())
            pass

          

async def addToRaffle(natural, forced, forceInfo = ""):
    global users
    
    if (forceInfo == "" and forced):
        await B.send_message("If you can see this, then the nerd who made this plugin did something wrong. Please inform him. He'll know!")
      
    if (forced and forceInfo != ""):
        if (len(forceInfo.mentions) > 0 and natural[2].startswith("@")):
            username = forceInfo.mentions[0].display_name
            numId = forceInfo.mentions[0].user_id
        
        elif (natural[2].startswith("#")):
            username = natural[2].lstrip("#").title()
            numId = 0

        else:
            await B.send_message("Unexpected input: '{}'! Manual entry cancelled.".format(natural[2]))
            return  

    elif (not forced):    
        username = natural.display_name
        numId = natural.user_id        
        
    for folks in users:
        if (folks == username):
            #print(folks)
            await B.send_message("Looks like you're already in the raffle, @{}!".format(username))
            return
            
    users.append(username)
    
    buffer = "{} successfully joined the raffle!".format(username)
       
    if (numId != 0):
        buffer = "@" + buffer
    
    await B.send_message(buffer)
    

    
    
async def removeFromRaffle(name):
    global users
    
    if (name.startswith("@")):
        name = name.lstrip("@")      
    elif(name.startswith("#")):
        name = name.lstrip("#")
    
    for nerds in users:
        if (name.lower() == nerds.lower()):
            users.remove(nerds)
            await B.send_message("{} has successfully been removed from the raffle.".format(nerds))
            return
    
    await B.send_message("Could not find the name \"{}\" among the entrants.".format(name))
    

    
    
async def sanitize_input(msg):
  try:
    msg.message = parser.unescape(msg.message)
    return msg
  except:
    print("Sanitize error")
        
    
    
async def output_phrase():
    await asyncio.sleep(1)
    await B.send_message("The key phrase is: [ {} ]".format(keyPhrase))

'''             
"open":ok
"close":ok
"clear": ok
"help":
"spin": ok
"redo":
"phrase":ok
"add": ok
"remove": ok
"blacklist": 
"leave" (for participants): ok
cooldown system
persistent tracking
'''