import httplib2
import json
import apiclient.discovery # pip install google-api-python-client
import names
from HTMLParser import HTMLParser #HTML STRIPPER


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


arr=[]
arr1=[]
MAX_RESULTS = 200 # Will require multiple requests
activity_results = []
API_KEY = 'AIzaSyAmKuPaBIPTMnkKGZBP5uDj_uJCKobSlRI' 
i=100


service = apiclient.discovery.build('plus', 'v1', http=httplib2.Http(), developerKey=API_KEY)
fh = open("gplus.txt","a")


while(i):
	Q = names.get_first_name() 
	people_feed = service.people().search(query=Q).execute()
	tasks = people_feed.get('items', [])
	for task in tasks:
		arr=task['id']
		arr1=task
		activity_feed = service.activities().list(userId=arr, collection='public', maxResults='100')
		while activity_feed != None and len(activity_results) < MAX_RESULTS:
			activities = activity_feed.execute()
			if 'items' in activities:
				for activity in activities['items']:
					if activity['object']['objectType'] == 'note' and activity['object']['content'] != '':
						activity['title'] = strip_tags(activity['title'])
						activity['object']['content'] = strip_tags(activity['object']['content'])
						activity_results += [activity]
						# list_next requires the previous request and response objects
			activity_feed = service.activities().list_next(activity_feed, activities)
		fh.write(json.dumps(arr1, indent=1))
		fh.write(json.dumps(activity_results, indent=1))
		fh.write('\n<====================================================><====================================================><====================================================>\n<====================================================><====================================================><====================================================>\n')
	i=i-1


fh.close()
print "Task Complete"

