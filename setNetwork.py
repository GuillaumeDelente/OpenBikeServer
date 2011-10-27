#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from network import *

class SetNetwork(webapp.RequestHandler):

    def get(self):
        if Network.all(keys_only = True).count() != 0:
            self.response.out.write('There already is a network for this server !')
        else:
            self.response.out.write("""
          <form action="/private/setNetwork" method="post">
            <div>id : <input type="text" name="id" /></div>
            <div>update url : <input type="text" name="update_url" /></div>
            <div>list url : <input type="text" name="list_url" /></div>
            <div><input type="submit" value="Save"></div>
          </form>
        </body>
      </html>""")
    
    def post(self):
       try:
           Network(id = int(self.request.get('id')),
                    update_url = self.request.get('update_url'), 
                    list_url = self.request.get('list_url')).put()
           self.response.out.write('Network set')
       except:
           self.response.out.write('Error setting network')

def get_network_from_datastore():
    network = db.GqlQuery("SELECT * "
                              "FROM network")
    memcache.set('network', network)
    return network
