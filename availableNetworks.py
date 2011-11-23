#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from availableNetwork import *

class AvailableNetworks(webapp.RequestHandler):

    def get(self, api_version = 1):
        networks = get_available_networks()
        if networks is None:
            self.error(500)
        else:
            self.response.headers["Content-Type"] = "application/json; charset=utf-8"
            self.response.out.write(networks)
