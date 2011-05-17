package fr.openbike;

import org.restlet.Application;
import org.restlet.Restlet;
import org.restlet.routing.Router;

import fr.openbike.serverresource.NetworksServerResource;
import fr.openbike.serverresource.StationsServerResource;
import fr.openbike.servlet.DeleteNetworks;
import fr.openbike.servlet.DeleteStations;
import fr.openbike.servlet.NewNetwork;
 
// Main server : used for Bordeaux and Network choice

public class OpenBikeServer extends Application {
 
    /**
     * Creates a root Restlet that will receive all incoming calls.
     */
    @Override
    public Restlet createInboundRoot() {

        Router router = new Router(getContext());
        // - Clean DB
        router.attach("/internal/cleanStations", DeleteStations.class);        
        
        // - Clean DB
        router.attach("/internal/cleanNetworks", DeleteNetworks.class);
        
        // - Insert Network
        router.attach("/internal/insertnetwork", NewNetwork.class);
        
        // - Update Vcub
        // Not called directly
        //router.attach("/internal/updateVcub", UpdateVcub.class);             
        
        // - Update
        //router.attach("/internal/update", Update.class);     
        
        // --- List of all stations ---
        // - Old url, only Bordeaux
        router.attach("/stations", StationsServerResource.class);
        // - New url
        router.attach("/stations/{city}", StationsServerResource.class);
        
        // --- A specific station --- Not yet needed
        //router.attach("stations/{city}/{station}", StationServerResource.class);
        
        // List of all networks - as it is the main server
        router.attach("/networks", NetworksServerResource.class);
        return router;
    }
}