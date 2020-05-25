
import requests, json
import subprocess
import sys

authorize_url = "https://oauth.picarto.tv/authorize"
token_url = "https://oauth.picarto.tv/token"

#callback url specified when the application was defined
callback_uri = "https://picarto.tv/"

test_api_url = "https://api.picarto.tv/"

#client (application) credentials - located at apim.byu.edu
client_id = ""
client_secret = ""

# simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.

authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri

print ("go to the following url on the browser and enter the code from the returned url: ")
print ("---  " + authorization_redirect_url + "  ---")
authorization_code = input('code: ')
print("code:\n" + authorization_code)

# turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri, 'client_id': client_id, "client_secret": client_secret}
print ("requesting access token\n")
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False)#, auth=(client_id, client_secret))

print ("response\n")
print (access_token_response.headers)


# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
print(tokens)
access_token = tokens['access_token']
print ("access token: " + access_token)

# Doesn't work with this scope yrt. :(
req = requests.get("https://api.picarto.tv/v1/user/jwtkey", headers={'Authorization': 'Bearer {}'.format(access_token)}, params={'channel_id':"", 'bot':'true'})
code = req.status_code
token = req.text
print ("Ta-Daaaa!\n")
print (token)