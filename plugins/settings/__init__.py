import asyncio
from src import Bunn as B


def init():
    pass
  
  
async def on_command(msg):  
  
  cmd = msg.message[1:].split(" ")
  # Remember, we're using spaces to split, so the comparison string won't have spaces in it.
  # Expected cmd split: 
  #[0] = error command, 
  #[1] = If None, that means the entire command is invalid, otherwise it's an invalid sub-command,
  #[2] = the original base command itself, 
  #[3:] = Everything after the base command which had an improper sub-command.
  # NOTE: These errors should only be returned when invalid COMMANDS are input, NOT when the ARGUMENTS of valid commands are invalid.
  
 
  if (cmd[0].upper() == "<COMMAND________ERROR>"):    
      if (cmd[1] == "0"):
          await B.send_message("Sorry, but \"{0}\" is an invalid \"{1}\" command.".format(" ".join(cmd[3:]), cmd[2]))
          
      elif (cmd[1] == "None"):
          await B.send_message("Sorry, but \"{}\" is an invalid command.".format(cmd[2]))

      # Usually, we grab cmd[0] for getting the command string, but since we injected text specifically for improper inputs,
      # we have to move over one additional index to get to the command the user ACTUALLY input.  