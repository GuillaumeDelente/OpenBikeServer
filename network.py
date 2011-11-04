from google.appengine.ext import db
from google.appengine.api import users, memcache
import logging

class Network(db.Model):
    id = db.IntegerProperty(required=True)
    update_url = db.StringProperty(required=True)
    list_url = db.StringProperty(required=True)
    data_version = db.IntegerProperty(default = 0)
    message = db.StringProperty(default = '')

def get_network():
    network = memcache.get('network')
    logging.error('Network : ' + str(network))
    if network is None:
        network = Network.all().get()
        if network is None:
            logging.error('lenth 0')
            return None
        logging.error('lenth not null')
        logging.error(str(network))
        memcache.set('network', network)
    return network
    
