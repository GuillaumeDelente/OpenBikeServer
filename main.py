from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from update import *
from stations import *
from fetchStations import *
from networks import *
from addNetwork import *
from setMessage import *

application = webapp.WSGIApplication([('/private/update', Update),
                                      ('/private/addNetwork', AddNetwork),
                                      ('/private/setMessage', SetMessage),
                                      ('/queue/fetchStations', FetchStations),
                                      ('^/networks/?$', Networks),
                                      ('^/stations/?$', Stations),
                                      ('^/stations/\d+/?$', Stations),
                                      ('^/v(\d+)/stations/?$', Stations),
                                      ('^/v(\d+)/stations/\d+/?$', Stations),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
