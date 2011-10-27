from google.appengine.ext import webapp
from google.appengine.api import memcache, taskqueue
from network import *

class UpdateList(webapp.RequestHandler):

    def get(self):
        network = memcache.get('network')
        if network is None:
            network = get_network_from_datastore()
        taskqueue.add(queue_name='fetchQueue', 
                      url='/queue/fetchStationList', 
                      params={'url': network.list_url, 'id': network.id})
        self.response.out.write('List update in progress')
