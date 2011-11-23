from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache, urlfetch, mail, users, app_identity, taskqueue
import math
from station import *
from updateUrl import *

class Update(webapp.RequestHandler):

    def get(self):
        stations = get_stations()
        if stations is None:
            return
        count = len(stations)
	to = int(math.ceil(count / 10))
	update_url = get_update_url()
        if update_url is None:
            mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                           to="contact@openbike.fr",
                           subject="No update url for slave",
                           body='No update url for slave')

        for i in range(0, to):
            taskqueue.add(queue_name='fetchQueue', 
                          url='/queue/fetchStations', 
                          params={'from': i, 'update_url': update_url}, method='POST')
        self.response.out.write("<html><body><p>Ok</p></body></html>")
