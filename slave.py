from google.appengine.ext import db
from google.appengine.api import users, memcache

class Slave(db.Model):
    slave_url = db.StringProperty(required=True)

def get_slaves_from_datastore():
    slaves = Slave.all().fetch(limit = 20)
    memcache.set('slaves', slaves)
    return slaves
