from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache, urlfetch, mail, users, app_identity, taskqueue
import math
from network import *
from station import *

class Update(webapp.RequestHandler):

    def get(self):
        taskqueue.add(queue_name='fetchQueue', 
                      url='/queue/fetchStations',
                      method='GET')
        self.response.out.write("<html><body><p>Ok</p></body></html>")
