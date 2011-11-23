#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from station import *

class Stations(webapp.RequestHandler):

    def get(self):
        stations = get_stations()
        if stations is None:
            self.response.out.write("<html><body><p>No stations</p></body></html>")
        else:
            self.response.out.write(
                simplejson.dumps(
                    [station.to_dict() for station in stations]))
