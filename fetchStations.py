from google.appengine.ext import webapp
from google.appengine.ext.deferred.deferred import PermanentTaskFailure
from google.appengine.api import memcache, urlfetch, mail, users, app_identity, taskqueue
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson
from BeautifulSoup import BeautifulStoneSoup
import logging, re
from station import *
from network import *

class FetchStations(webapp.RequestHandler):

    def get(self):
        try:
            network = get_network();
            if network is None:
                logging.error(
                    'No network set')
                self.error(200)
                return
            result = urlfetch.fetch(network.list_url, deadline = 10, method='POST', payload='xml=<gpsinfo><methodname>updateStations</methodname></gpsinfo>')
        except urlfetch.DownloadError:
            logging.error('Timeout')
            self.error(200)
            return
        if result.status_code != 200:
            logging.error(
                'Unable to reach list webservice, error '
                + str(result.status_code))                
            mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
                           to="contact@openbike.fr",
                           subject="Paris problem",
                           body="Impossible to get stations list with error code " + str(result.status_code) + " for paris")
            self.error(200)
            return

        soup = BeautifulStoneSoup(result.content, fromEncoding="utf-8")
        print soup.originalEncoding
        xml_stations = soup.findAll('stationinfo')
        stations = get_stations()
        mobile_stations = get_mobile_stations()
        if mobile_stations is None:
            mobile_stations = set()
        new_mobile_stations = set()
        new_stations = []
        parsed_ids = set()
        update_mobile = False
        if stations is None:
            stations = {}
        for xml_station in xml_stations:
            id = int(xml_station.nb.string)
            slots = int(xml_station.freebs.string)
            bikes = int(xml_station.freebk.string)
            open = bool(xml_station.state.string == 'open')

            parsed_ids.add(id)
            station = stations.get(id)

            if station is not None:
                station.availableBikes = bikes
                station.freeSlots = slots
                station.open = open
                if (id is in mobile_stations):
                    if (station.latitude != float(xml_station.lat.string) or
                        station.longitude != float(xml_station.lng.string)):
                        update_mobile = True
                        latitude = float(xml_station.lat.string)
                        longitude = float(xml_station.lng.string)
                        address = unicode(xml_station.sadd.string).title()
            else:
                new_station = Station(id = id, 
                        name = re.compile('[^a-zA-Z]*(.*)').match(unicode(xml_station.lb.string)).group(1).title(),
                        address = unicode(xml_station.sadd.string).title(),
                        open = open,
                        payment = True,
                        special = bool(xml_station.bonusflag.string == "1"),
                        network = network.id,
                        latitude = float(xml_station.lat.string),
                        longitude = float(xml_station.lng.string),
                        availableBikes = bikes,
                        freeSlots = slots)
                if ('Station Mobile' in new_station.name):
                    new_mobile_stations.add(new_station.id)
                new_stations.append(new_station)
                stations[id] = new_station
        if len(new_stations) != 0:
            db.put(new_stations)
        if update_mobile:
            mobiles = [stations[id] for id in mobile_stations]
            db.put(mobiles)
        to_remove = set(stations.keys()).difference(parsed_ids)
        for id in to_remove:
            station = stations.pop(id)
            station.delete()
        if len(to_remove) != 0:
            mobile_stations = mobile_stations.difference(to_remove)
            memcache.set('mobile_stations', mobile_stations)
        memcache.set('stations', stations)
        if len(new_mobile_stations) != 0:
            memcache.set('mobile_stations', mobile_stations.union(new_mobile_stations))
        self.response.out.write("<html><body><p>OK</p></body></html>")
