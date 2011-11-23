from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache

class Station(db.Model):
    id = db.IntegerProperty(required=True)
    freeSlots = db.IntegerProperty(default=0)
    availableBikes = db.IntegerProperty(default=0)
    payment = db.BooleanProperty(default=False)

    def to_dict(self):
        return {"id": self.id, 
                "availableBikes": self.availableBikes,
                "freeSlots": self.freeSlots,
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
        memcache.set('stations', stations)
        return stations
    else:
        return None
