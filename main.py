from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from update import *
from stations import *
from fetchStations import *
from setStations import *

application = webapp.WSGIApplication([('/private/update', Update),
                                      ('/setStationsIds', SetStations),
                                      ('/queue/fetchStations', FetchStations),
                                      ('^/stations/?$', Stations),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
