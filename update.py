from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache, urlfetch, mail, users, app_identity, taskqueue
import math, logging
from network import *
from station import *
from slave import *


class Update(webapp.RequestHandler):

    def get(self):
        stations = get_stations()
        if stations is None:
            self.redirect('/private/updateList')
            return
        slaves = get_slaves()
        if slaves is None:
            logging.error('No slaves !')
	for slave in slaves:
		taskqueue.add(queue_name='fetchQueue', 
			      url='/queue/fetchStations', 
			      params={'slave_url': slave.slave_url},
			      method='POST')
        self.response.out.write("<html><body><p>Ok</p></body></html>")
