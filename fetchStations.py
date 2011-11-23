from google.appengine.ext import webapp
from google.appengine.api import memcache, urlfetch, mail, users, app_identity
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json
from BeautifulSoup import *
import logging
from station import *

class FetchStations(webapp.RequestHandler):

    def post(self):
        def handle_result(result):
            if result.status_code == 200:
                update_stations(result.content)
            elif result.status_code == 403:
                logging.error('403 fetching station')
                mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                               to="contact@openbike.fr",
                               subject="Access denied",
                               body="Access denied for app " + app_identity.get_application_id())
            else:
                logging.error(str(result.status_code) + ' fetching station')
                logging.error('Unable to reach webservice ' 
                              + str(result.status_code) 
                              + ' for content : ' 
                              + result.content 
                              + ' for station ' 
                              + id)

        def update_stations(content):
            stations = get_stations()
            #should not append, already checked before update launch
            if stations is None:
                return
#            try:
            parsed_stations = json.loads(content)
            for parsed_station in parsed_stations: 
                station = stations[int(parsed_station['id'])]
                if station is not None:
                    station.availableBikes = parsed_station['availableBikes']
                    station.freeSlots = parsed_station['freeSlots']
                    station.payment = parsed_station['payment']
            memcache.set('stations', stations)

        url = self.request.get('slave_url')
        handle_result(urlfetch.fetch(url + '/stations'))
        self.response.out.write("<html><body><p>OK</p></body></html>")
