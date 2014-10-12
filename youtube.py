from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError #pip install google-api-python-client
from oauth2client.tools import argparser #pip install oauth2client
import json


DEVELOPER_KEY = '' 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

argparser.add_argument("--q", help="Search term", default="Swag mera desi")
argparser.add_argument("--max-results", help="Max results", default=25)
args = argparser.parse_args()
options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
search_response = youtube.search().list(q=options.q, type="video", part="id,snippet", maxResults=options.max_results).execute()

videos = {}
for search_result in search_response.get("items", []):
 if search_result["id"]["kind"] == "youtube#video":
#videos.append("%s" % (search_result["id"]["videoId"]))
   videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

#print "Videos:\n", "\n".join(videos), "\n"
s = ','.join(videos.keys())
videos_list_response = youtube.videos().list(id=s, part='id,statistics').execute()

res = []
for i in videos_list_response['items']:
 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
 temp_res.update(i['statistics'])
 res.append(temp_res)
 #Getting Search_Feed
print json.dumps(videos_list_response, indent=1)
