from google.appengine.ext import webapp
from google.appengine.api import memcache, taskqueue, urlfetch, mail, users, app_identity
from BeautifulSoup import *
from station import *
from network import *
import logging, math, urllib

class FetchStationList(webapp.RequestHandler):

    def post(self):
        url = self.request.get('url')
        network_id = int(self.request.get('id'))
        try:
            result = urlfetch.fetch(url, deadline = 10)
        except urlfetch.DownloadError:
            logging.error('Timeout for list update')
            self.error(200)
            return
	if result.status_code != 200:
            logging.error(
                'Unable to reach list webservice, error '
                + str(result.status_code))
            mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                           to="contact@openbike.fr",
                           subject="Station list access",
                           body="Error " + str(result.status_code) + ' for ' + app_identity.get_application_id())
            self.error(200)
            return
	soup = BeautifulStoneSoup(result.content)
        new_ids = set()
        old_ids = set()
        force_update = False
        stations = get_stations()
        if stations is not None:
            old_ids = set(stations.keys())
        else:
            stations = {}
            force_update = True
        version_upgrade = False
	#inserting
        new_stations = []
        #try:
        for marker in soup.markers.findAll('marker'):
            parsed_id = int(marker['id'])
            new_ids.add(parsed_id)
            if force_update or (parsed_id not in old_ids):
                version_upgrade = True
                station = (Station(availableBikes = 0, 
                                   freeSlots = 0, 
                                   network = network_id, 
                                   name = marker['name'],
                                   id = parsed_id,
                                   longitude = float(marker['lng']), 
                                   latitude = float(marker['lat']), 
                                   open = True, 
                                   payment = False, 
                                   special = False))
                #Add to cache
                stations[parsed_id] = station
                #Collect new stations for datastore
                new_stations.append(station)
#        except:
#            mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
#                           to="contact@openbike.fr",
#                           subject="Station list",
#                           body="Error parsing station list content " + str(result.status_code) + ' for ' + app_identity.get_application_id())            
        #closed stations
        closed_ids = old_ids.difference(new_ids)
        for closed_id in closed_ids:
            stations[closed_id].open = False
        if len(new_stations) != 0:
            save_stations_to_datastore(new_stations)
        memcache.set('stations', stations)

	if version_upgrade:
	#increment data version
            network = Network.all().get()
            network.data_version += 1
            network.put()
            memcache.set('network', network)
        self.response.out.write('ok')
        return
