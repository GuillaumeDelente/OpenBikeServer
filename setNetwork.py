#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from network import *
from station import *

class SetNetwork(webapp.RequestHandler):

    def get(self):
        network = get_network()
        if network is not None:
            self.response.out.write('There already is a network for this server !<br />')
            self.response.out.write('ID : ' + str(network.id) + '<br />')
            self.response.out.write('List url : ' + network.list_url + '<br />')

        self.response.out.write("""
          <form action="/private/setNetwork" method="post">
            <div>id : <input type="text" name="id" /></div>
            <div>list url : <input type="text" name="list_url" /></div>
            <div><input type="submit" value="Save"></div>
          </form>
        </body>
      </html>""")

    def post(self):
        try:
            network = get_network()
            if network is not None:
                memcache.delete('network')
                network.delete()
                stations_dict = get_stations()
                stations = stations_dict.values()
                db.delete(stations)
            
            Network(id = int(self.request.get('id')),
                    list_url = self.request.get('list_url')).put()
            self.response.out.write('Network set')
        except:
            self.response.out.write('Error setting network')
