#downloading captions from playlist
#Dustin Henderson

#Dustin Henderson

# Sample Python code for user authorization

import httplib2
import os
import sys
import copy
import urllib
import lxml

import urllib2
import re

#from difflib import SequenceMatcher

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from lxml import etree
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl import load_workbook

	

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0" 

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("youtube-api-snippets-oauth2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))


args = argparser.parse_args()
service = get_authenticated_service(args)

def print_results(results):
  print(results)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]
      # Convert a name like "snippet.tags[]" to snippet.tags, but handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True
      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

### END BOILERPLATE CODE

# Sample python code for playlistItems.list

def playlist_items_list_by_playlist_id(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
  results = service.playlistItems().list(
    **kwargs
  ).execute()
  return(results)

def findNextToken (apiResponce):
	token = ""
	start = 0
	end = 0
	if(apiResponce.find('nextPageToken') != -1):
		start = apiResponce.find('nextPageToken') + 18
		end = apiResponce[start:].find('\'')
		print "start: ", start
		print "end: ", end
		token = apiResponce[start:end+start]
		return token
	else:
		return "*"
		
def findVidID (apiResponce):
	id = ""
	start = 0
	end = 0 
	start = apiResponce.find('videoId\'') + 12
	end = start + 11
	print "start: ", start
	print "end: ", end
	print "vid ID: ", apiResponce[start:end]
	return apiResponce[start:end]
	
		
def getFileLocation():
	enteredLoc = ""
	goodPath = False
	print "***********************************************************"
	print "Please enter file location for the captions to be saved in"
	print "saved in (Example: C:\Users\dustinhe\Videos\e3eCaptions\)"
	enteredLoc = raw_input("location: ")
	while(goodPath == False):
		if not os.path.exists(enteredLoc):
			print "bad path"
		else:
			print "***********************************************************\n\n"
			return enteredLoc
		enteredLoc = raw_input("location: ")
		
def getListId():
	enteredLoc = ""
	print "***********************************************************"
	print "Please enter YoutTube playlist ID"
	print "Example: PL0pU5hg9yniZn8VpD1jRNWK6dlAucCMDR"
	enteredLoc = raw_input("Playlist ID: ")
	print "***********************************************************\n\n"
	return enteredLoc
	
'''************* edit *******************'''
def videos_list_by_id(service, **kwargs):
	kwargs = remove_empty_kwargs(**kwargs)
	results = service.videos().list(
	**kwargs
	).execute()
	return results
	
def getTitle(vidId):
	results = ""
	results = str(videos_list_by_id(	service,
									part='snippet',
									id=vidId))
	#print results
	start = results.find('title\'') + 10
	end = results[start:].find('\'') + start
	#print "\n"
	return results[start:end]
	
def download_caption(youtube, caption_id, tfmt):
	subtitle = youtube.captions().download( id=caption_id, tfmt=tfmt).execute()
	
# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-api-captions.json", "r") as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))
	
'''*********************************** Main Part of Script ***********************************'''
playListId = ""
fileLocation = ""
token = ""
videoId = ""
counter = 0
lastToken = False

youtube = get_authenticated_service(args) #added to try and get captions api working

fileLocation = getFileLocation()
print "test id currently: PLYYARuW-EUbEzCScH6unajic_fkaOG7Yv" #my test playlist
playListId = getListId()
apiResponce = str(playlist_items_list_by_playlist_id(service, part='contentDetails', maxResults=1, playlistId=playListId))
token = findNextToken(apiResponce)
print token
videoId = findVidID(apiResponce)
print getTitle(videoId)

download_caption(youtube, videoId, 'srt')

while(lastToken == False):
	apiResponce = str(playlist_items_list_by_playlist_id(service, pageToken=token, part='contentDetails', maxResults=1, playlistId=playListId))
	print "\n"
	print apiResponce
	print "\n"
	token = findNextToken(apiResponce)
	videoId = findVidID(apiResponce)
	print getTitle(videoId)
	if((token == "*")):
		lastToken = True
	'''************* For Testing ********************'''
	
	'''**********************************************'''
	
	print token
	counter = counter + 1 
	print "number of videos", counter + 1
	
	getTitle("https://www.youtube.com/watch?v=39RcJg8Auwg&index=22&list=PLYYARuW-EUbEzCScH6unajic_fkaOG7Yv")
	
exit()




