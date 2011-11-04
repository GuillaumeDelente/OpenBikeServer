from google.appengine.ext import db
from google.appengine.api import users, memcache
from django.utils import simplejson
import logging

class Status(db.Model):
    data_version = db.IntegerProperty(required=True)
    message = db.StringProperty(required=False, default='')

    def to_dict(self):
        if len(self.message) == 0:
            return {"version": self.data_version}
        else:
            return {"version": self.data_version,
                    "message": self.message}

def get_status():
    status = memcache.get('status')
    if status is None:
        status = Status.all().get()
        if status is None:
            status = Status(data_version=0)
            status.put()
            memcache.set('status', status)
        return status
    else:
        return status
