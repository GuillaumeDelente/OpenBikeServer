from google.appengine.ext import db
from google.appengine.api import users, memcache

class Network(db.Model):
    id = db.IntegerProperty(required=True)
    update_url = db.StringProperty(required=True)
    list_url = db.StringProperty(required=True)
    data_version = db.IntegerProperty(default = 0)
    message = db.StringProperty(default = '')

def get_network_from_datastore():
    network = Network.all()[0]
    memcache.set('network', network)
    return network
