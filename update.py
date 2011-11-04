from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache, urlfetch, mail, users, app_identity, taskqueue
import math
from network import *
from station import *

class Update(webapp.RequestHandler):

    def get(self):
        stations = get_stations()
        if stations is None:
            return
        keys = stations.keys()
        count = len(keys)
	to = int(math.floor(count / 10)) + 1
        network = get_network()
	update_url = network.update_url
	for i in range(0, to):
		taskqueue.add(queue_name='fetchQueue', 
			      url='/queue/fetchStations', 
			      params={'update_ids': '-'.join(str(id) for id in keys[i*10:i*10+10]), 'update_url': update_url},
			      method='POST')
        self.response.out.write("<html><body><p>Ok</p></body></html>")
