from google.appengine.ext import webapp
from google.appengine.api import memcache, taskqueue, urlfetch, mail, users, app_identity
from BeautifulSoup import *
from station import *
from slave import *
from setupSlaves import *
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
                           subject="Station list acces",
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
	#inserting
        new_stations = []
        try:
            for marker in soup.carto.markers.findAll('marker'):
                parsed_id = int(marker['number'])
                new_ids.add(parsed_id)
                if force_update or (parsed_id not in old_ids):
                    station = (Station(availableBikes = 0, 
                                       freeSlots = 0, 
                                       network = network_id, 
                                       name = re.compile('[^a-zA-Z]*(.*)').match(marker['name']).group(1).title(),
                                       id = parsed_id, 
                                       address = marker['address'].title(), 
                                       longitude = float(marker['lng']), 
                                       latitude = float(marker['lat']), 
                                       open = True, 
                                       payment = False, 
                                       special = bool(int(marker['bonus']))))
                #Add to cache
                    stations[parsed_id] = station
                #Collect new stations for datastore
                    new_stations.append(station)
                else:
                    stations[parsed_id].open = True
        except:
            mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                           to="contact@openbike.fr",
                           subject="Station list acces",
                           body="Error " + str(result.status_code) + ' for ' + app_identity.get_application_id())            
        #closed stations
        closed_ids = old_ids.difference(new_ids)
        for closed_id in closed_ids:
            stations[closed_id].open = False
        memcache.set('stations', stations)
        if len(new_stations) != 0:
            save_stations_to_datastore(new_stations)
            setup_slaves()
        return
                
