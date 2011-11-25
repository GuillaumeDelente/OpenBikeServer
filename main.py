from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from update import *
from stations import *
from stationsList import *
from fetchStations import *
from setNetwork import *
from setMessage import *
from addNetwork import *
from availableNetworks import *

application = webapp.WSGIApplication([('/private/update', Update),
                                      ('/private/setNetwork', SetNetwork),
                                      ('/private/setMessage', SetMessage),
                                      ('/private/addNetwork', AddNetwork),
                                      ('/queue/fetchStations', FetchStations),
                                      ('^/networks/?$', AvailableNetworks),
                                      ('^/v(\d+)/networks/?$', AvailableNetworks),
                                      ('^/stations/?$', StationsList),
                                      ('^/stations/\d+/?$', StationsList),
                                      ('^/v(\d+)/stations/?$', Stations),
                                      ('^/v(\d+)/stations/list/?$', StationsList),],
                                     debug=True)




def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
