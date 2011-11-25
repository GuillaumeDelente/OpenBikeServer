#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from django.utils import simplejson
from google.appengine.api import memcache
from google.appengine.ext.webapp.util import run_wsgi_app
from network import *
from station import *

class StationsList(webapp.RequestHandler):

    def get(self, api_version = 1, id = 0, full = False):
        stations = get_stations()
        if stations is None:
            self.response.out.write(u"{\"message\": \"Les données sont momentanément indisponible, réessayez dans quelques instants.\",\"stations\": []}")
        else:
            self.response.headers["Content-Type"] = "application/json; charset=utf-8"           
            if api_version == 1:
                json = simplejson.dumps(
                    [station.to_full_dict() for station in stations.values()])
                self.response.out.write(json)
                return
            else:
                network = get_network()
                message = network.message
                response = ["{\"version\": ", str(network.data_version), ", "]
                if len(message) != 0:
                    response.append("\"message\": \"")
                    response.append(message)
                    response.append("\", ")
                response.append("\"stations\": ")
                response.append(simplejson.dumps(
                        [station.to_full_dict() for station in stations.values()]))
                response.append("}")
                self.response.out.write(''.join(response))
