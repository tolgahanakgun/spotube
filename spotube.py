import spotipy
import json
import subprocess
from spotipy.oauth2 import SpotifyClientCredentials
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

SPOTIFY_USERNAME = 'AUSERNAME'
SPOTIFY_PLAYLIST_ID = 'APLAYLISTID'
SPOTIPY_CLIENT_ID='XXXXXXXXXXXXX'
SPOTIPY_CLIENT_SECRET='XXXXXXXXXXXXX'
YOUTUBE_DEVELOPER_KEY = "XXXXXXXXXXXXX"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=YOUTUBE_DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet",
    maxResults=max_results,
    location=location,
    locationRadius=location_radius

  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result)
  try:
      nexttok = search_response["nextPageToken"]
      return(nexttok, videos)
  except Exception:
      nexttok = "last_page"
      return(nexttok, videos)

def get_spotify_list(username, playlist_id):
  client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
  sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

  results = sp.user_playlist(username, playlist_id)

  playlist = []

  for item in results['tracks']['items']:
      artist = ', '.join([x.get('name') for x in item.get('track').get('artists')])
      playlist.append(artist+' - '+item.get('track').get('name'))
    
  return playlist


spotify_playlist = get_spotify_list(SPOTIFY_USERNAME, SPOTIFY_PLAYLIST_ID)

youtube_list = []

for song in spotify_playlist:
  video = youtube_search(song)[1][1]
  youtube_list.append(video['id']['videoId'])
     
command = 'youtube-dl.exe'

for song in youtube_list:
  subprocess.call([command, '-i', '-f', 'bestaudio[ext=m4a]', '-o', '"%(title)s.%(ext)s"',song])
 