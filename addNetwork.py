#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from availableNetwork import *

class AddNetwork(webapp.RequestHandler):

    def get(self):
        networks = get_available_networks()
        self.response.out.write("""
          <form action="/private/addNetwork" method="post">
            <div>id : <input type="text" name="id" /></div>
            <div>name : <input type="text" name="name" /></div>
            <div>city : <input type="text" name="city" /></div>
            <div>server : <input type="text" name="server" /></div>
            <div>latitude : <input type="text" name="latitude" /></div>
            <div>longitude : <input type="text" name="longitude" /></div>
            <div>specialName : <input type="text" name="specialName" /></div>
            <div><input type="submit" value="Save"></div>
          </form>
        </body>
      </html>""")
    
    def post(self):
        try:
            AvailableNetwork(id = int(self.request.get('id')),
                    name = self.request.get('name'), 
                    city = self.request.get('city'),
                    server = self.request.get('server'),
                    latitude = float(self.request.get('latitude')),
                    longitude = float(self.request.get('longitude')),
                    specialName = self.request.get('specialName')).put()
            memcache.delete('available_networks')
            self.response.out.write('Network added !')
        except:
            self.response.out.write('Error adding network')
