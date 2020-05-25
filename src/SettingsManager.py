import os
import sys
import json
from src import Bunn as B


plugin_folder = "./plugins"
streamer_folder = "./streamers"

control_plugin_name = "settings"
settings_file= "settings.json"


def __init__(self):
    self.settings = {}
  
  

def init_settings_list(self, path):
    try:
        self.settings = {}    
        plugin_list = os.listdir(plugin_folder)

        for i in plugin_list:      
            path = os.path.join(plugin_folder, i)
            if not os.path.isdir(path) or not settings_file in os.listdir(path):
                continue                
            self.load_settings(path, i, False)                  
            
        print("Settings loaded successfully!")
        return self.settings
      
    except:
        print("Error searching settings file.")
        raise
  
    
      
def load_settings(self, path, plugin_name, override = False):
    try:
        with open(path,'r') as settings_file:               
            if (plugin_name in self.settings and override == False):
                print("Warning: Settings already exist for \"{}\". Skipping...".format(key))
            
            elif (plugin_name == control_plugin_name):
                print("Skipping settings controller plugin...")
                
            else:
                self.settings[plugin_name] = json.load(settings_file)                     
                print("Settings loaded for plugin: {}!".format(plugin_name))
        
    except:
        print("Error loading settings file for plugin: {}".format(plugin_name))
        raise

# Remember to impliment a "settings profile" options! In addition to the streamer's usual settings,
# allow them to swap to a completely different set that they created and saved. 

# Also remember to save only the CHANGES in the settings files to the streamer 
# folder; no need to make a file that will go unused. Have the settings file in the plugin folder
# simply be the default settings.

# Holy hexx use JSONs for storing data based on user PLEASE (also backups). Formatting is a waste
# of time, resources, energy, and debugging effort

# When settings are changed, save them both to the active client AND the streamer's user folder.
# Do not refer to files onsce client has booted; use client's internal copy of the settings.
