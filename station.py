from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

class Station(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    address = db.StringProperty(default='')
    freeSlots = db.IntegerProperty(default=0)
    availableBikes = db.IntegerProperty(default=0)
    payment = db.BooleanProperty(default=False)
    network = db.IntegerProperty(required=True)
    latitude = db.FloatProperty(required=True)
    longitude = db.FloatProperty(required=True)
    open = db.BooleanProperty(default=True)
    special = db.BooleanProperty(default=False)
    
    
    def to_full_dict(self):
        return {"id": self.id, 
                "name": self.name,
                "availableBikes": self.availableBikes,
                "freeSlots": self.freeSlots,
                "open": self.open,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "address": self.address, 
                "payment": self.payment,
                "special": self.special,
                "network": self.network}

    def to_dict(self):
        return {"id": self.id, 
                "availableBikes": self.availableBikes,
                "freeSlots": self.freeSlots,
                "open": self.open,
                "network": self.network}


def save_stations_to_datastore(stations):
    db.put(stations)

def get_stations():
    stations = memcache.get('stations')
    if stations is not None:
        return stations
    count = Station.all().count()
    if count != 0:
        stations = Station.all().fetch(count)
        stations = dict([(station.id, station) for station in stations])
        memcache.set('stations', stations)
        return stations
    else:
        return None
