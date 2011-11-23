from google.appengine.ext import db
from google.appengine.api import memcache

class UpdateUrl(db.Model):
    updateUrl = db.StringProperty(required=True)

def save_update_url_to_datastore(url):
    db.put(UpdateUrl(url))

def get_update_url():
    update_url = memcache.get('update_url')
    if update_url is not None:
        return update_url.updateUrl
    update_url = Station.all().get()
    if update_url is not None:
        memcache.set('update_url', update_url)
        return update_url.updateUrl
    else:
        return None
