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
    version = db.IntegerProperty(default=1)

    def to_dict(self):
        return {"id": self.id, 
                "name": self.name,
                "server": self.server,
                "city": self.city,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "specialName": self.specialName}

    def to_dict_v1(self):
        return {"id": self.id, 
                "name": self.name,
                "server": self.server + "/stations/",
                "city": self.city,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "specialName": self.specialName}

def get_available_networks(version):
    networks = memcache.get('available_networks' + str(version))
    json = ""
    list = []
    if networks is None:
        networks = AvailableNetwork.all().order('city').fetch(100)
        if version == 1:
            for network in networks:
                if version >= network.version:
                    list.append(network.to_dict_v1())
            json = simplejson.dumps(list)
        else:
            for network in networks:
                if version >= network.version:
                    list.append(network.to_dict())
            json = simplejson.dumps(list)
        memcache.set('available_networks' + str(version), json)
        return json
    else:
        return networks
