#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from slave import *

class AddSlave(webapp.RequestHandler):

    def get(self):
        self.response.out.write("""
          <form action="/private/addSlave" method="post">
            <div>Slave url : <input type="text" name="slave_url"></div>
            <div><input type="submit" value="Add"></div>
          </form>
        </body>
      </html>""")
    
    def post(self):
       try:
           Slave(slave_url = self.request.get('slave_url')).put()
           memcache.delete('slaves')
           self.response.out.write('Slave added')
       except:
           self.response.out.write('Error adding slave')
