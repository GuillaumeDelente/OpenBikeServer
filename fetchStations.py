from google.appengine.ext import webapp
from google.appengine.api import memcache, urlfetch, mail, users, app_identity
from google.appengine.ext.webapp.util import run_wsgi_app
from BeautifulSoup import *
import logging
from station import *

class FetchStations(webapp.RequestHandler):

    def post(self):
        def handle_result(rpc, id):
            result = rpc.get_result()
            if result.status_code == 200:
                update_station(id, result.content)
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

	# Use a helper function to define the scope of the callback.
        def create_callback(rpc, id):
            return lambda: handle_result(rpc, id)

	def update_station(id, content):
            soup = BeautifulStoneSoup(content)
            try:
                parsed_station = soup.station
                to_update = stations[int(id)]

                to_update.availableBikes = int(parsed_station.bikes.string)
                to_update.freeSlots = int(parsed_station.attachs.string)
                to_update.payment = parsed_station.paiement.string == 'AVEC_TPE'
                if len(to_update.address) == 0:
                    to_update.address = parsed_station.adress.string.title()
                to_update.open = parsed_station.status.string == '0'
            except:
                logging.error('error parsing station with content ' + content)
                mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                               to="contact@openbike.fr",
                               subject="Parsing Error",
                               body='Error while parsing ' + id + ' with content ' + content)

        url = self.request.get('update_url')
        update_ids = [id for id in self.request.get('update_ids').split('-')]
	stations = get_stations()
        #Should not append as we check before launching update
        if stations is None:
            return
	rpcs = []
        try:
            for id in update_ids:
                rpc = urlfetch.create_rpc(deadline = 10)
                rpc.callback = create_callback(rpc, id)
                urlfetch.make_fetch_call(rpc, url + id)
                rpcs.append(rpc)
            for rpc in rpcs:
                rpc.wait()
            memcache.set('stations', stations)
        except urlfetch.DownloadError:
            logging.error('Time out fetching stations')
            self.error(500)
            return
        self.response.out.write("<html><body><p>OK</p></body></html>")
