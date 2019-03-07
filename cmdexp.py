from concurrent import futures


def task(n):
    print('{}: starting'.format(n))
    #raise ValueError('the value {} is no good'.format(n))


ex = futures.ThreadPoolExecutor(max_workers=2)
print('main: starting')
f = ex.submit(task, 5)

error = f.exception()
print('main: error: {}'.format(error))

#try:
#    result = f.result()
#except ValueError as e:
#    print('main: saw error "{}" when accessing result'.format(e))


"""
import sys
import asyncio
from asynccmd import Cmd


#from cmd import Cmd

class MyPrompt(Cmd):
  
    def __init__(self, mode, intro, prompt):
        # We need to pass in Cmd class mode of async cmd running
        super().__init__(mode=mode)
        self.intro = intro
        self.prompt = prompt
        self.loop = None

    def do_hello(self, args):
        ""Says hello. If you provide a name, it will greet you with it.""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print ("Hello, %s" % name)

    def do_exit(self, args):
        ""Quits the program.""
        print ("Quitting.")
        raise KeyboardInterrupt
        
    def start(self, loop=None):
        # We pass our loop to Cmd class.
        # If None it try to get default asyncio loop.
        self.loop = loop
        # Create async tasks to run in loop. There is run_loop=false by default
        super().cmdloop(loop)
        

loop = asyncio.get_event_loop()
mode = "Reader"
# create instance
cmd = MyPrompt(mode=mode, intro="This is example", prompt="example> ")
cmd.start()  # prepare instance
try:
    loop.run_forever()  # our cmd will run automatically from this moment
except KeyboardInterrupt:
    loop.stop()
        
'''
if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
'''
"""