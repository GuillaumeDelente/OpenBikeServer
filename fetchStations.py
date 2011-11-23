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
        def create_callback(rpc, i):
            return lambda: handle_result(rpc, i)

        def update_station(stations, index, content):
            soup = BeautifulStoneSoup(content)
            try:
                parsed_station = soup.station
                stations[index].availableBikes = int(parsed_station.available.string)
                stations[index].freeSlots = int(parsed_station.free.string)
                stations[index].payment = bool(int(parsed_station.ticket.string))   
            except:
                mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                               to="contact@openbike.fr",
                               subject="Parsing Error",
                               body='Error while parsing ' + str(station.id) + ' with content ' + content)
        url = self.request.get('update_url')
        result_from = int(self.request.get('from'))
	from_index = result_from * 10
	stations = get_stations()
        #Should not append as we check before launching update
        if stations is None:
            return
        sub_stations = stations[from_index:from_index + 10]
	rpcs = []
        i = from_index	
        try:
            for station in sub_stations:
                rpc = urlfetch.create_rpc()
                rpc.callback = create_callback(rpc, i)
                urlfetch.make_fetch_call(rpc, url + '/' + str(station.id))
                rpcs.append(rpc)
                i += 1
            for rpc in rpcs:
                rpc.wait()
            memcache.set('stations', stations)
        except urlfetch.DownloadError:
            logging.error('Time out fetching stations')
            self.error(500)
            return
        self.response.out.write("<html><body><p>OK</p></body></html>")
