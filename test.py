import datetime


def score(name):  
  peek = ""
  found = False
  
  score = open("scoreboard.txt", "r")  
  temp = open("temp.txt", "w") 
  date = datetime.datetime.now()
  date = "{0}, {1}/{2}/{3}, {4}:{5} {6}".format(date.strftime("%A"), date.strftime("%B"), date.strftime("%d"), date.strftime("%Y"), date.strftime("%I"), date.strftime("%M"), date.strftime("%p"))
  
  temp.seek(0)
  temp.truncate()

  for line in score:
      if (line.strip() == name):
          found = True
          temp.write(name + "\n")
          peek = score.readline()
          pip = 1 

          while (len(peek) > 0 and peek[0].isdigit() and peek.startswith(".) ", 1)):
              temp.write(peek)
              pip = str(int(peek[0]) + 1)
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


  
  
print("Opening score!")
score("Molly")
print("\nDone reading score.")

'''
Molly
Nerds
Bricks
'''
