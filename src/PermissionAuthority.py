import json
import asyncio

class PermissionAuthority():
    def __init__(self):
        # Permissions formatting:
        #   command : permission level
        self.permissions = {}

    def load_permissions(self, path, override = False):
        try:
            with open(path,'r') as perm_file:
                jsondata = json.load(perm_file)
                for i in range(len(jsondata)):
                    key = list(jsondata.keys())[i]
                    if (key in self.permissions and override == False):
                        print("Warning: Permission definitions already exist for \"{}\". Skipping...".format(key))
                    else:
                        self.permissions[key] = jsondata[key]
                        ###print(self.permissions[key])
            print("Permissions loaded")
        except:
            print("Error loading permission file.")
            raise

    async def async_load_permissions(self, path, override=False):
        try:
            with open(path,'r') as perm_file:
                jsondata = json.load(perm_file)
                for i in range(len(jsondata)):
                    key = list(jsondata.keys())[i]                    
                    ###print(key)
                    if (key in self.permissions and override == False):
                        print("Warning: Permission definitions already exist for \"{}\". Skipping...".format(key))
                    else:
                        self.permissions[key] = jsondata[key]
            print("Permissions loaded")
        except:
            print("Error loading permission file.")
            raise

    async def parse_permission_level(self,perm):
        # We might actually have a number
        if (isinstance(perm,int)):
            return perm

        perm = perm.lower()

        if (perm == "everyone" or perm == "all" or perm == "0"):
            return 0
        elif (perm == "registered" or perm == "users" or perm == "1"):
            return 1
        elif (perm == "basic" or perm == "2"):
            return 2
        elif (perm == "premium" or perm == "3"):
            return 3
        elif (perm == "subscriber" or perm == "sub" or perm == "4"):
            return 4
        elif (perm == "moderator" or perm == "mod" or perm == "5"):
            return 5
        elif (perm == "streamer" or perm == "admin" or perm == "6"):
            return 6
        else:
            return 7

    async def retrieve_permission_level(self, perms, args, is_list=False):
        # perms is a list of things.
        # Perms would be: self.permissions["filter"] which = ["add","remove","help"]

        # args is the list of arguments passed in.
        # e.g. [filter, add, word]
        #if (is_list == False):
        #    key = list(perms.keys())[0]
        #else:
        #    key = 0
        #print(args)
        #print(perms)
        key = args[0]

        #try:
            #print(args[0])
            #print(perms)
            #print(perms[key])
            #print(key)
        #except:
        #    pass

        try:
            if (isinstance(perms[key],list)):
                return await self.parse_permission_level(perms[key][0])
            # If we've hit a string or an int, we're done.
            if (isinstance(perms[key], str) or isinstance(perms[key], int)):
                return await self.parse_permission_level(perms[key])

            else:
                # If we haven't hit a string or int yet, and we've only got one entry, then
                # we know it's a list.
                # This is to ease potential formatting woes
                # e.g.: "filter":[{"add":1,"remove":1,"help":1}]
                if (len(perms[key]) == 1):
                    return await self.retrieve_permission_level(perms[key][0],args[1:])
                else:
                    if key in perms:
                        # We check perms[args[0]] which is the equivalent of:
                        # permissions["filter"] for the start, for instance,
                        # given perms = self.permissions{} and args = [filter,add,word]
                        # This would return a list of: [add[], remove[], help[]]
                        # Then we pass it in a cut-down list of args. So, [add,word]
                        # So the next time around, we'll be checking [add[], [remove[], help[]]
                        # to see if it includes anything at "add"
                        return await self.retrieve_permission_level(perms[key],args[1:])
                    else:
                        # By default only streamers/admins will have access to this command.
                        return 2
        except KeyError:
            return 2

    async def check_permissions(self, cmd, userlvl):

        # We'll cut off the ! from the command we're given.
        cmd = cmd[1:]      
        
        # split it into individual commands
        args = cmd.split(" ")
        
        if(len(args) == 1):
            args.append("")
            print(args)

        # We'll run retrieve_permission_level to get the permission level of the command
        permission = await self.retrieve_permission_level(self.permissions,args)
        # If we meet the required level to use this command, we'll return true
        if (userlvl >= permission):
            return True

        return False

    async def get_permission_level(self, msg):
        perm_level = 0
        if (msg.registered):
            perm_level = 1
        if (msg.basic):
            perm_level = 2
        if (msg.premium):
            perm_level = 3
        if (msg.subscriber):
            perm_level = 4
        if (msg.moderator):
            perm_level = 5
        if (msg.streamer):
            perm_level = 6
        if (msg.ptv_admin):
            perm_level = 7
        return perm_level
