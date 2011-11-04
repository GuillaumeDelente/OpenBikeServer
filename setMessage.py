#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from network import *

class SetMessage(webapp.RequestHandler):

    def get(self):
        network = get_network()
        self.response.out.write('''
          <form action="/private/setMessage" method="post">
            <div>Message : <input type="text" name="message" value="'''
                                + network.message + '''"
                                /></div>
            <div><input type="submit" value="Save"></div>
          </form>
        </body>
      </html>''')
    
    def post(self):
        try:
            network = get_network()
            network.message = self.request.get('message')
            network.put()
            memcache.set('network', network)
            self.response.out.write('Message set !')
        except:
            self.response.out.write('Error setting message')
