from google.appengine.ext import db
from google.appengine.api import users, memcache

class Slave(db.Model):
    slave_url = db.StringProperty(required=True)

def get_slaves():
    slaves = memcache.get('slaves')
    if slaves is not None:
        return slaves
    slaves = Slave.all().fetch(limit = 20)
    memcache.set('slaves', slaves)
    return slaves
