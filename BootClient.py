#shlex.quote() on ALL user input!!!! Or shell injection happens
# "nohup python Main.py & " command allows for process to run in the background, without need for console open
"""
# Assuming Python 3.

class Politician:

    def __init__(self, name, age=45):
        self.name = str(name)
        self.age = age
        self.votes = 0

    def change(self):
        self.votes = self.votes + 1

    def __str__(self):
        return '{}: {} votes'.format(self.name, self.votes)

num_politicians = int(input("The number of politicians: "))
politicians = []
for n in range(num_politicians):
    if n == 0:
        new_name = input("Please enter a name: ")
    else:
        new_name = input("Please enter another name: ")
    politicians.append(Politician(new_name)) <<<<<< Is how we instance clients

print('The Number of politicians: {}'.format(len(politicians)))
for politician in politicians:
    print(politician)

print('Processing ...')
for x in range(100):
    pol = random.choice(politicians)
    pol.votes += 1

for politician in politicians:
    print(politician)
"""