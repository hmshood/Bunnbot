'''
>Mail!<
-Since Picarto doesn't have an offline message system, why not make one locally for chats?
-Main use is to send messages to offline folks
-Will need a "address book", which logs people into it as soon as they type one message into chat
-This address book can be called upon with a command, which the bot will whisper back to you
-It will be in alphabetical order, and broken up over several whispers if need be
-This allows users to accurately enter users' names without the autocomplete if they're offline 
-The bot will detect if youre trying to send mail to someone not in the address book, spitting an error, but saving the text.
-The user can then change the reciever of that draft without having to retype their message
-Until a user whispers a (DONE), cnsecutive whispers to the bot will be part of the same message, allowing for longer rambles
-Any messages that are sent in without having the last (DONE) command will be saved into a "drafts" inbox, which will remember the info
-In case of spam or the user needing to send another message to the bot, the user can interrupt the bot with a (HOLD) or (EXIT)
   -The former command temporaily stops the playback/read and saves it to accept more commands, the second going back to the inbox
??To send messages across different channels, the bot will periodically check to see if the "times checked" counter is the same as it left it


-Whenever a user joins a channel, the bot will see if they are the address book. If so, they check their mail status.
    -If it detects unread messages (items that not have been set to True and moved to the back of the array by (READ) or (DONE)), 
    it'll increment the unread counter until it reads the first True labeled message, returning the number.
      [You have [2] unread messages! Whisper !mail to see more.]
      
    <INBOX> Commands: OPEN [category], SEND [username], USERS | 
    [2] New, [12] Old, [2] Drafts, [0] Blocked
    
-If the user whispers the command to the bot, it'll whisper back the categories of: New, Old, Drafts, and Blocked, with how many of each (#)
-Once in any category outside of Draft, the user will get a list in the format:
   1-[Inline: Jan.3/19] It'll give a conca...
   2-[CewlJoke: Mar.24/19] Depending on th...
   (Page 1/3)
   
-And so on. Users can go NEXT, PREV, FIRST, LAST, and PAGE # to navigate, EXIT to go to categories. 
    -Open messages using READ #, and delete DELETE #. Delete current page with DELETE PAGE, otherwise DELETE PAGE #. To empty, DELETE ALL.
    -Older messages get pushed further down as newer ones come in.
    
-Drafts will have the format:
    1-[To: Inline, Apr.3, 2pgs] This is a draft all about h...
    2-[To: Fridge, Dec.6, 16pgs] About how my draft got flip...
-Blocked will be in the format:
    [Blocked Users(#)]: Oneguy, loudmouth, skeet
    yeet, wokeadope, nardbard (Page 1/6)
-Blocked users cannot send messages to whoever blocked them, the bot shutting them down as soon as they start to compose a message.
- When composing a message, you must be in the menu level and send the bot SEND USERNAME, which the bot will whisper back if the user exists:

   [Now Composing to (USERNAME)] Commands: DONE, EXIT, EDIT #, DELETE. Whisper with no commands to add to the letter.
   
-When sent:
      [MESSAGE SENT SUCCESSFULLY]
  or  [FAILED TO DELIVER. SAVED TO DRAFTS]
  OR  [MAIL SERVICE DOWN, ALERT STREAMER]

-Allow the streamer to use a SEND * command, which will send a message to ALL users in the address book. Useful for announcing delays or dates?

-Maybe have messages be


Character limit: 255


'''