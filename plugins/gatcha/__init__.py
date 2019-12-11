import sys
import asyncio
import datetime
import tempfile
import random
from pytz import timezone
from src import Bunn as B
from src import Consts as C
import html.parser as htmlparser

parser = htmlparser.HTMLParser()      # Used to keep non-alphanumeric characters in output reable and not an encoded mess.
users = []      
keyDefault = "???"                    # This is the default key phrase used to enter the raffle once it's open. DO NOT CHANGE AT PLUGIN RUNTIME
keyPhrase = keyDefault                # The ACTUAL key phrase that'll be used to compare to entrants' input
active = False                        # True = raffle open for key phase entires. False = no more entrants accepted unless force added via coroutine.
charLimit = 255
winner = ""

oddsOn = True                         # Determines if raffles will cause the luck compensation to update.
oddsInit = 1                          # Initial amount of entries a new user has when first participating in a raffle.
oddsAdd = 1                           # Amount of entries that the raffle losers gain after a roll.
oddsMinus = -1                        # Here for whatever reason/situation you need to decriment a stack
oddsReset = 0                         # Amount of entries the raffle winner's stack will be reduced to after a roll.
oddsAuto = 50                         # Number of entries before an entrant automatically wins the raffle. Mercy win, basically.



def init():                       
    global users
    global oddsOn
    
    f = open("raffle.txt", "r+")      # Check if there are any previous existing entries into the raffle. This is to handle the bot shutting down mid raffle.
  
    if (len(f.read()) > 0):           # If there is anything on file, put each line from that into the current raffle queue.
        f.seek(0)
        for line in f:
            users.append(line.strip())
            
    f.close()    
    
    g = open("toggles.txt", "r+")     # Clunky way to add raffle state persisteance in case of bot shutdown. If there's anything written to file, the Luck mechanic is enabled.
    if (len(g.readline()) == 0):
        oddsOn = False  
    g.close()




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
                          
        remove <name>:    Same format and process as in the above "add" command, but removes someone from the current raffle entry list.
                         
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
  
  # Check if message contains keyword anyhwere.  
  if (active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1 and msg.message[0] != C.command_char and not msg.streamer):
      await addToRaffle(msg, False)
  elif (not active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1):
      await B.send_message("No open raffle to join yet!")      

      
      
      
async def on_raffle_run(msg):
    global winner
    global users
    buffer = ""    
  
    await score(msg.winner)
    winner = msg.winner    
    
    # Look up the winner's username from the entry list, updating everyone's score in a huma readable format.    
    if (oddsOn):    
        for nerd in users:     
            odds = open("stacked_odds.txt", "r")
            check = open("temp_odds.txt", "w")
            for line in odds:                

                if (nerd.strip() == line[(line.find("]") + 2):].strip()):
                    currStack = int(line[1:(line.find("]"))]) 

                    if (nerd.lower() != winner.lower()):                       
                        currStack += oddsAdd                           

                    elif (nerd.lower() == winner.lower()):
                        currStack = oddsReset

                    
                    buffer += " {0}: [{1}] |".format(nerd.strip(), str(currStack))
                    check.write("[" + str(currStack) + "] " + nerd + "\n")

                else:
                    check.write(line)


            odds.close()
            odds = open("stacked_odds.txt", "w")

            check.close()
            check = open("temp_odds.txt", "r")

            odds.write(check.read())        
            odds.close()
            check.close()   
        
        
    
    await asyncio.sleep(6)   # Wait for animation to play client side, as the winner is chosen instantly, but the roll is in real time and is just for show.
    await B.send_message(":tada: Congrats, @{} you've won the raffle! :tada:".format(msg.winner))
    
    if (oddsOn):
        await asyncio.sleep(4)
        await B.send_message(":four_leaf_clover: The rest of you guys gain [" + str(oddsAdd) + "] extra entry(s) for your next raffle as compensation! :four_leaf_clover:")
        
        await asyncio.sleep(2)           
        await B.send_message("Here are your new standings: ")
        
        await asyncio.sleep(3)
        buffer = buffer.strip("|")
        await B.send_message(buffer)

            
  
  
  
async def on_command(msg):
    global users
    global active
    global keyPhrase
    global oddsOn
    
    #print("1")
    #print(oddsOn)
  
    # Retrieve the message'scontents, scrub it for potencial plain-text injections, 
    #and split it into an array of whole words, ignoring the command character.
    
    msg = await sanitize_input(msg)
    cmd = msg.message[1:].split(" ")
      

    if (cmd[0].lower() == "gatcha"):
        try:
            if (len(cmd) == 1):              
                if (active and keyPhrase != "???"):
                    await output_phrase()
                elif (active and keyPhrase == "???"):
                    await B.send_message("Oops! There's a raffle open, but there's no key phrase set! Kindly ask your host to set one using the '{0}{1} phrase' command!".format(C.command_char, cmd[0]))
                else:
                    await B.send_message("There are no raffles open at this time.")
                    
                    
            elif (len(cmd) > 1):
                smallCmd = cmd[1].lower()
              
                if (smallCmd == "open" or smallCmd == "sesame"):
                    if (smallCmd == "sesame"):
                        extraCmd = cmd[2:]
                        extraCmd = " ".join(extraCmd)
                        keyPhrase = extraCmd
                        users = []
                        
                        f = open("raffle.txt", "w+")
                        f.write("")
                        f.close()
                        
                        await B.send_message("POOF! Keyword changed and list of entries wiped!")
                        await asyncio.sleep(2)
                  
                    if (not active):
                        if (smallCmd == "open"):
                            active = True
                        await B.send_message("Okay, guys! Get ready! The raffle's about to open again!")

                    if (keyPhrase == "???"):
                        await asyncio.sleep(1)
                        await B.send_message("Oh! Well. The raffle is open, but remember to set the key phrase using the '{0}{1} phrase' command!".format(C.command_char, cmd[0]))
                    elif (keyPhrase != "???"):
                        await asyncio.sleep(1)
                        await B.send_message("On your marks!")
                        await asyncio.sleep(1)
                        await B.send_message("Get set!")
                        await asyncio.sleep(3)
                        await B.send_message(":checkered_flag::checkered_flag:Go!:checkered_flag::checkered_flag:")
                        
                        active = True
                        
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
                            await B.send_message("There is no key phrase at this time. Please set one using the '{0}{1} phrase' command!".format(C.command_char, cmd[0]))                  
                        else:
                            print("Unexpected value for key phrase: {}".format(keyPhrase))                              
                      
                      
                      
                      
                elif (smallCmd == "reset"):
                    buffer = ""
                    active = False

                    if (len(users) > 0):
                        users = []
                        
                        f = open("raffle.txt", "w+")
                        f.write("")
                        f.close()
                        
                        buffer = "The list of raffle entrants has been reset"
                    else:
                        buffer = "The current list of raffle entrants is already empty "                    

                    if (keyPhrase != "???"):
                      keyPhrase = "???"
                      buffer += " AND its key phrase has been reset!"
                    elif (keyPhrase == "???"):
                      buffer += " BUT the key phrase remains blank."
                  
                    await B.send_message(buffer)
                  
                  
                  
                  
                elif (smallCmd == "list"):
                      print(":(")
                      print(oddsOn)
                      print(":)")
                      if (len(users) > 0):
                          if (oddsOn):
                              buffer = ""
                              total = 0

                              for entrant in users:
                                  stacks = await stackDisplay(entrant)                                   
                                  if (not stacks):
                                      stacks = oddsInit

                                  total += int(stacks)                                  
                                  buffer += " {0}: [{1}] |".format(entrant, stacks)     
                                  

                              
                              await B.send_message("[Current Entrants ({0}) | Total Luck ({1})]:".format(len(users), total))
                              await asyncio.sleep(1)
                              buffer = buffer.strip("|")
                              await B.send_message(buffer)
                              
                          else:
                              buffer = "[Current Raffle Entrants ({})]:".format(len(users))

                              for nerds in users:
                                  buffer += " {},".format(nerds.strip())
                              buffer = buffer.strip(",")
                              await B.send_message(buffer)
                              
                      else:
                          await B.send_message("There are no entrants to list.")

                          
                          
                          
                          
                elif (smallCmd == "add" or smallCmd == "ban" or smallCmd == "unban" or smallCmd == "lookup"):
                    if (len(cmd) == 2 and smallCmd == "lookup"):
                        buffer = "[BLACKLISTED Users]: "                      
                        
                        with open("blacklist.txt", "r") as black:
                            length = len(black.read())   
                            
                            black.seek(0)
                        
                            if (length <= 0):
                                await B.send_message("Blacklist is currently empty! :tada:")
                                return

                            else:
                                for line in black:  
                                    #print(line.strip())
                                  
                                    if (len(buffer) + len(line) + 3 > charLimit): #The 3 here represent two space and comma
                                        buffer = buffer.strip(",")
                                        await B.send_message(buffer)
                                        buffer = line.strip()
                                    else:
                                        buffer += "{}, ".format(line.strip())
                                    
                                buffer = buffer.rstrip(" ,")
                                await B.send_message(buffer)
                  
                    elif (len(cmd) == 3 and (cmd[2].startswith("@") or cmd[2].startswith("#"))):
                        result = None
                        name = cmd[2][1:].title()
                        
                      
                        if (smallCmd == "add"):
                            await addToRaffle(cmd, True, msg)     # Format: (Parsed command split into pieces, Is forced, Raw message object)               
                            
                        #Format for "parse_blacklist": (name, #) 
                        #Where # is: 0 = Read list, 1 = Add to blacklist, 2 = remove from blacklist, 3 compare against list of entrants
                        elif (smallCmd == "lookup"):
                            result = await parse_blacklist(name, 0) 
                            
                            if (result):
                                await B.send_message("User \"{}\" is currently BLACKLISTED.".format(name))
                            else:
                                await B.send_message("User \"{}\" not found on the blacklist.".format(name))
                                
                                
                        elif (smallCmd == "ban"):
                            result = await parse_blacklist(name, 1)
                            if (result):
                                await B.send_message("User \"{}\" is now BLACKLISTED. They cannot join future raffles.".format(name))
                                await addToRaffle(name, False, "ban")
                            else:
                                await B.send_message("Error adding user \"{}\" to the blacklist. Please try again.".format(name))
                                
                        elif (smallCmd == "unban"):
                            result = await parse_blacklist(name, 2)
                            
                            if (result):
                                await B.send_message("User \"{}\" has been successfully removed from the blacklist.".format(name))
                            else:
                                await B.send_message("Error removing user \"{}\" from the blacklist. Please try again.".format(name))
                            
                    else:
                        await B.send_message("Improper input! Please try again using: '{0}{1} {2} @<username>' for named entrants or '{0}{1} {2} #<name>' for anonymous ones!".format(C.command_char, cmd[0], cmd[1]))
                
                
                
                
                elif (smallCmd == "remove"):
                    if (len(cmd) == 3):
                        await removeFromRaffle(cmd[2].title())
                    else:
                        await B.send_message("Improper input! Try again using the format of: '{0}{1} {2} username'!".format(C.command_char, cmd[0], cmd[1]))
                
                
                
                
                elif (smallCmd == "leave"):
                      await removeFromRaffle(msg.display_name.title())
                  
                  
                  
                  
                elif (smallCmd == "luck"):  
                    stacks = await stackDisplay(msg.display_name)
                    
                    if (stacks):
                        await B.whisper(msg.display_name, ":four_leaf_clover:@{0}, you have [{1}] stacks of luck.:four_leaf_clover:".format(msg.display_name, stacks))
                    elif(stacks == False):
                        await B.whisper(msg.display_name, "@{}, you must have participated in a raffle to start gaining luck stacks!".format(msg.display_name))
                        
                        
                        
                        
                elif (smallCmd == "toggle"):     
                    
                    g = open("toggles.txt", "w+")                        
                    oddsOn = not oddsOn                    
                    if (oddsOn):
                        g.write(str(oddsOn))
                    g.close()                   
                   
                    
                    await B.send_message("{0} has been set to {1}".format("Luck", oddsOn))                   
                  
                  
                  
                  
          
                elif (smallCmd == "spin" or smallCmd == "reroll"):
                    global winner
                    
                    if (len(winner) > 0 and smallCmd == "reroll"):
                        await removeFromRaffle(winner)
                        await asyncio.sleep(1)
                  
                    if (len(users) > 1):                       
                        await B.send_message("Raffle spinning! Good luck, guys!")                        
                                 
                        if (oddsOn):
                            mixedUsers = await stackEm(users.copy())
                            print("ON :" + str(len(mixedUsers)))
                        else:
                            mixedUsers = users.copy()
                            print("OFF: " + str(len(mixedUsers)))
                            
                        i = len(mixedUsers) - 1    
                        #print(str(i))
                        

                        while (i > 0):
                            toSwap = random.randint(0, i)
                            temp = mixedUsers[i]
                            mixedUsers[i] = mixedUsers[toSwap]
                            mixedUsers[toSwap] = temp
                            i -= 1

                        await asyncio.sleep(3)
                        await B.raffle_init(mixedUsers)

                    elif (len(users) <= 1):
                        await B.send_message("Sorry, but there aren't enough users for a raffle! You need at least 2 people!")
                
                else:
                    await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0].lower()))
                                                        
                                             
        except:
            print("Error in gatcha.")
            print(sys.exc_info())
            pass

          
          

async def addToRaffle(natural, forced = False, forceInfo = ""):
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

    elif (not forced and forceInfo != "ban"):    
        username = natural.display_name
        numId = natural.user_id    
    elif (not forced and forceInfo == "ban"):
        username = natural
  
    isBanned = await parse_blacklist(username, 3)
    
    if (isBanned):
        buffer = "@{}, you are currently blacklisted. You will not be allowed to".format(username.title())
        
        if (forced):
            buffer = "User \"{}\" is currently blacklisted and cannot".format(username.title())
            
        await B.send_message("[[DENIED ENTRY]] {0} enter raffles unless a host undoes it with: {1}gatcha unban".format(buffer, C.command_char))
        await removeFromRaffle(username, True)
        return
              
    for folks in users:
        if (folks == username):
            await B.send_message("Looks like you're already in the raffle, @{}!".format(username))
            return
            
    users.append(username)
    
    buffer = "{0} successfully joined the raffle!".format(username)
    
    if (not forced):
        buffer = buffer + " To leave type: {}gatcha leave".format(C.command_char)
       
    if (numId != 0):
        buffer = "@" + buffer
        
    f = open("raffle.txt", "w+")
    
    for line in users:
        f.write(line + "\n")
        
    f.close()
    
    await B.send_message(buffer)
    

    
    
async def removeFromRaffle(name, isBanned = False):
    global users
    
    if (name.startswith("@")):
        name = name.lstrip("@")      
    elif(name.startswith("#")):
        name = name.lstrip("#")
    
    for nerds in users:
        if (name.lower() == nerds.lower()):
            users.remove(nerds)
            
            f = open("raffle.txt", "w+")    
            for line in users:
                f.write(line + "\n")
                
            await B.send_message("{} has successfully been removed from the raffle.".format(nerds))
            return
    
        
    if (not isBanned):
        await B.send_message("Could not find the name \"{}\" among the entrants.".format(name))
    


    
async def sanitize_input(msg):
  try:
    msg.message = parser.unescape(msg.message)
    return msg
  except:
    print("Sanitization error.")
        
    
    
    
async def output_phrase():
    await asyncio.sleep(1)
    await B.send_message("The key phrase is: [ {} ]".format(keyPhrase))
    
    
    

async def parse_blacklist(name, editFlag):
    # editFlag values: 0 = lookup only, 1 = add name, 2 = delete name  
    found = False
    black = open("blacklist.txt", "r")
    addMe = name
    peek = ""
    #print("OH MY")
  
    with tempfile.TemporaryFile(mode = "w+") as copy:
        for line in black:           
            if (line == "\n"):
                continue
          
            if (line.strip().lower() == name.lower()):     
                found = True
              
                if (editFlag == 0): #read only
                    print("entered 0")
                    return found                
                elif (editFlag == 1): #add name
                    print ("Name already present on list.")
                    return False                
                elif (editFlag == 2): #"remove" name by ignoring on copy
                    continue    
                elif (editFlag == 3):
                    print("ENEMY SPOTTED")
                    return True
                else:
                    print("Unexpected editFlag code. Aborting process.")
                    return None
                  
            copy.write(line + "\n")
            
        if (not found):
            if (editFlag == 0):
                print("exit 0")
                return False
            elif (editFlag == 1):
                print("exit 1")
                copy.write(addMe.title())
                print("exit 11")
            elif (editFlag == 2):
                print("exit 2")
                return False
            elif (editFlag == 3):
                return False
            else:
                print("Unexpected editFlag value. Aborting process.")
                return None
              
        
        black.close()
        black = open("blacklist.txt", "w")
                     
        copy.seek(0)
                     
        black.write(copy.read().replace("\n\n", "\n").lstrip())
        black.close()
        return True
    
    
    
    
async def stackEm(list):
    blocks = open("stacked_odds.txt", "r")
    newList = []
    found = False    
    
    
    for name in list:
        #print("Init: " + name)
        #print(name)
        found = False
        for line in blocks:     
            #print("Name: " + name + " Line: " + line)    
            if (name.lower().strip() == line[(line.find("]") + 2):].lower().strip()):  # Seperate the username from the "[#]" score by 
                found = True                                                           # finding the index closing bracket and moving
                for x in range(int(line[1:(line.find("]"))])):                         # the pointer two places over; one to skip the "]"
                    if (0 < int(line[1:(line.find("]"))])):                            # and the second to skip the space, leaving the pointer
                        newList.append(name)                                           # right next to the start of the username.
                #break
                
        if (not found):                           # If the user is not currently on the luck tracking list, add them to it with the default starting value.
            #print("Not found :(")
            blocks.close()                
            blocks = open("stacked_odds.txt", "a")          
            blocks.write("[" + str(oddsInit) + "] " + name + "\n")
            blocks.close()
            blocks = open("stacked_odds.txt", "r")
            for y in range(oddsInit):
                newList.append(name)  
            
        blocks.seek(0)
    
    blocks.close()
    print("DURING: " + str(len(newList)))
    return(newList)
         
    
    

async def stackDisplay(name):
    odds = open("stacked_odds.txt", "r")
    for line in odds: 
        #print(line)
        if (name.lower().strip() == line[(line.find("]") + 2):].lower().strip()):           
            odds.close()
            return(str(line[1:(line.find("]"))]))

    odds.close()
    return(False)
    

    
             
async def score(name):  
  peek = ""
  found = False
  
  score = open("scoreboard.txt", "r")  
  temp = open("temp.txt", "w") 
  
  eastern = timezone('US/Eastern')
  date_east = datetime.datetime.now(eastern)
  
  date = datetime.datetime.now()
  date = "{0}, {1}/{2}/{3}, {4}:{5} {6} ({7}:{8} {9} EST)".format(
  date.strftime("%A"), date.strftime("%B"), date.strftime("%d"), date.strftime("%Y"), 
  date.strftime("%I"), date.strftime("%M"), date.strftime("%p"), 
  date_east.strftime("%I"), date_east.strftime("%M"), date_east.strftime("%p"))
  
  temp.seek(0)
  temp.truncate()

  for line in score:
      if (line.strip() == name):
          found = True
          temp.write(name + "\n")
          peek = score.readline()
          pip = 1 

          while (len(peek) > 0 and peek[0].isdigit() and (peek.find(".)") > -1)):  #peek.startswith(".) ", 1)):
              nextdig = -1
              
              if(peek[1].isdigit()):
                  pip = int(peek[0]) * 10 + int(peek[1]) + 1
              else:
                  pip = int(peek[0]) + 1
              
              temp.write(peek)
              peek = score.readline()

          temp.write(str(pip) + ".) " + date + "\n")
          temp.write(peek)
          
          if (int(pip) > 32):
              return
  
      else:
          temp.write(line)
        
  if (found == False):
      temp.write("\n" + name + "\n1.) " + date + "\n")
          
  temp.close()   
  temp =  open("temp.txt", "r") 
  
  score.close()
  score = open("scoreboard.txt", "w")  

  score.write(temp.read())
  score.close()
  temp.close()

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
"blacklist": ok
"leave" (for participants): ok
cooldown system:
persistent tracking: ok

bounty:
  claim
  post
  list - default (!gatcha bounty)
'''