import html.parser as htmlparser


def score(name):  
  
  score = open("scoreboard.txt", "r")  
  temp =  open("temp.txt", "w") 
  parser = htmlparser.HTMLParser() 
  offset = 0
  anchor = 0

  temp.seek(0)
  temp.truncate()

  for line in score:
      if (line.strip() == name):
          temp.write(name + "\n")
          peek = score.readline()
          pip = 1 

          while (len(peek) > 0 and peek[0].isdigit() and peek.startswith(".) ", 1)):
              temp.write(peek)
              pip = str(int(peek[0]) + 1)
              peek = score.readline()


          temp.write(str(pip) + ".) \n")
          temp.write(peek)
          
          if (int(pip) > 32):
              return

      else:
          temp.write(line)
          
  temp.close()   
  temp =  open("temp.txt", "r") 
  
  score.close()
  score = open("scoreboard.txt", "w")  

  score.write(temp.read())
  score.close()
  temp.close()


  
  
print("Opening score!")
score("Nerds")
print("\nDone reading score.")

'''
Molly
Nerds
Bricks
'''
