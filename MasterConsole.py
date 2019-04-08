import rpyc
from src.bunnbot import Console

c = rpyc.connect("localhost", 1111)

_master_console = Console.BunnConsole(mode="Reader", intro="[MASTER CONSOLE]", prompt=">>> ")