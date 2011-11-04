from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from update import *
from updateList import *
from stations import *
from fetchStations import *
from fetchStationList import *
from setNetwork import *
from setMessage import *

application = webapp.WSGIApplication([('/private/update', Update),
                                      ('/private/updateList', UpdateList),
                                      ('/private/setNetwork', SetNetwork),
                                      ('/private/setMessage', SetMessage),
                                      ('/queue/fetchStationList', FetchStationList),
                                      ('/queue/fetchStations', FetchStations),
                                      ('^/stations/?$', Stations),
                                      ('^/stations/\d+/?$', Stations),
                                      ('^/v(\d+)/stations/?$', Stations),
                                      ('^/v(\d+)/stations/\d+/?$', Stations),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
