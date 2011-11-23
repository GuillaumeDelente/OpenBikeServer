from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from update import *
from updateList import *
from stations import *
from stationsList import *
from fetchStations import *
from fetchStationList import *
from setNetwork import *
from setMessage import *
from addSlave import *

application = webapp.WSGIApplication([('/private/update', Update),
                                      ('/private/updateList', UpdateList),
                                      ('/private/setNetwork', SetNetwork),
                                      ('/private/setMessage', SetMessage),
                                      ('/private/addSlave', AddSlave),
                                      ('/queue/fetchStationList', FetchStationList),
                                      ('/queue/fetchStations', FetchStations),
                                      ('^/stations/?$', StationsList),
                                      ('^/stations/\d+/?$', StationsList),
                                      ('^/v(\d+)/stations/?$', Stations),
                                      ('^/v(\d+)/stations/list/?$', StationsList),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
