from google.appengine.ext import db
from google.appengine.api import users, memcache

class Network(db.Model):
    id = db.IntegerProperty(required=True)
    update_url = db.StringProperty(required=True)
    list_url = db.StringProperty(required=True)
    data_version = db.IntegerProperty(default = 0)
    message = db.StringProperty(default = '')

def get_network():
    network = memcache.get('network')
    if network is None:
        network = Network.all().get()
        if network is None:
            return None
        memcache.set('network', network)
    return network
    
