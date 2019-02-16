import configparser
import os
from src import Config as C

def load_configuration():
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    C.channel_name = cfg['account']['streamer']
    C.bot_channel_name = cfg ['account']['bot']
    C.access_token = cfg['account']['access_token']

    C.command_char = cfg['settings']['command_character']
    C.enable_multistream = cfg['settings']['enable_multistream']

    C.socket_url = cfg['picarto']['chat_url'] + 'socket?token={}'
    C.api_url = cfg['picarto']['api_url']
    C.api_v = cfg['picarto']['api_version']
