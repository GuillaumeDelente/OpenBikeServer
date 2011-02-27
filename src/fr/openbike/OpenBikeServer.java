package fr.openbike;

import org.restlet.Application;
import org.restlet.Restlet;
import org.restlet.routing.Router;
 
public class OpenBikeServer extends Application {
 
    /**
     * Creates a root Restlet that will receive all incoming calls.
     */
    @Override
    public Restlet createInboundRoot() {

        Router router = new Router(getContext());
        // List of all stations
        router.attach("/stations", StationsServerResource.class);
        // A given station
        router.attach("/stations/{station}", StationServerResource.class);
        return router;
    }
}