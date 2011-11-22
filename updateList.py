from google.appengine.ext import webapp
from google.appengine.api import memcache, taskqueue
from network import *
import logging

class UpdateList(webapp.RequestHandler):

    def get(self):
        network = get_network()
        if network is None:
            logging.error('No network')
            self.error(500)
            return
        taskqueue.add(queue_name='fetchQueue', 
                      url='/queue/fetchStationList', 
                      params={'url': network.list_url, 'id': network.id})
        self.response.out.write('List update in progress')
