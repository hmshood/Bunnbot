import configparser
import os
from src import Consts as C

def load_configuration():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    C.channel_name = cfg['account']['streamer']
    C.bot_channel_name = cfg ['account']['bot']
    C.access_token = cfg['account']['access token']

    C.command_char = cfg['settings']['command character']

    C.socket_url = cfg['picarto']['chat url'] + 'socket?token={}'
    C.api_url = cfg['picarto']['api url']
    C.api_v = cfg['picarto']['api version']
