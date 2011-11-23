from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from station import *
from updateUrl import *
import logging, re, os

class SetStations(webapp.RequestHandler):

    def post(self):
        if not os.environ['SERVER_SOFTWARE'].startswith('Development'):
            if not re.match(r'openbikeserver-?\d+\.appspot\.com', self.request.headers['Host']):
                self.error(401)
                return
        new_ids = [int(id) for id in self.request.get('stations_ids').split('-')]
        stations = get_stations()
        if stations is not None:
            new_set = set(new_ids)
            old_set = set([station.id for station in stations])
            to_delete = old_set.difference(new_set)
            stations[:] = [station for station in stations if station.id not in to_delete]
            to_add = new_set.difference(old_set)
            for new_id in to_add:
                stations.append(Station(id = new_id))
            memcache.set('stations', stations)
            self.response.out.write("<html><body><p>Ok with cache</p></body></html>")
        else:
            stations = []
            for new_id in new_ids:
                stations.append(Station(id = new_id))
            memcache.add("stations", stations)
            save_stations_to_datastore(stations)
            update_url = self.request.get('update_url')
            memcache.add("update_url", update_url)
            save_update_url_to_datastore(update_url)
            self.response.out.write("<html><body><p>Ok without cache</p></body></html>")
