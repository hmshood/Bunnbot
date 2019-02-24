'''
6.) YOINK. Dumb game which randomly picks a word said by a user into chat and lies in wait. When a user trips it, 
the bot will call out YOINK. Randomly from the next few users who !yoink 'd , that player now have The Goods, 
unbeknownst to the others. The Goods allow for that player to know what the trap word is. T
he Good-holder's job is to trick other users into saying this word. To win,they must make other users trip the trap 5 times. 
However, if someone is able to guess the work (!yoink trapWordHere), then the word is reset and the process repeats, 
with the players keeping their Trap Trip score.

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

8.) The only things announced in public are the basic rules and whether or not the (?) is up for grabs


    
    




'''