#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from status import *
from station import *

class Stations(webapp.RequestHandler):

    def get(self, api_version = 1, id = 0, full = False):
        stations = get_stations()
        if stations is None:
            self.response.out.write(u"{\"message\": \"Les données sont momentanément indisponible, réessayez dans quelques instants.\"}")
        else:
            self.response.headers["Content-Type"] = "application/json; charset=utf-8"
            status = get_status()
            message = status.message
            response = ["{\"version\": ", str(status.data_version), ", "]
            if len(message) != 0:
                response.append("\"message\": \"")
                response.append(message)
                response.append("\", ")
            response.append("\"stations\": ")
            response.append(simplejson.dumps(
                    [station.to_dict() for station in stations.values()]))
            response.append("}")
            self.response.out.write(''.join(response))
