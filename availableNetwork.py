from google.appengine.ext import db
from google.appengine.api import users, memcache
from django.utils import simplejson

class AvailableNetwork(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    server = db.StringProperty(required=True)
    city = db.StringProperty(required=True)
    latitude = db.FloatProperty(required=True)
    longitude = db.FloatProperty(required=True)
    specialName = db.StringProperty(required=True)

    def to_dict(self):
        return {"id": self.id, 
                "name": self.name,
                "server": self.server,
                "city": self.city,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "specialName": self.specialName}

def get_available_networks():
    networks = memcache.get('available_networks')
    if networks is None:
        networks = AvailableNetwork.all().order('city').fetch(100)
        json = simplejson.dumps(
            [network.to_dict() for network in networks])
        memcache.set('available_networks', json)
        return json
    else:
        return networks
