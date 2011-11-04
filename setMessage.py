#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.api import memcache
from status import *

class SetMessage(webapp.RequestHandler):

    def get(self):
        status = get_status()
        self.response.out.write('''
          <form action="/private/setMessage" method="post">
            <div>Message : <input type="text" name="message" value="'''
                                + status.message + '''"
                                /></div>
            <div><input type="submit" value="Save"></div>
          </form>
        </body>
      </html>''')
    
    def post(self):
        try:
            status = get_status()
            status.message = self.request.get('message')
            status.put()
            memcache.set('status', status)
            self.response.out.write('Message set !')
        except:
            self.response.out.write('Error setting message')
