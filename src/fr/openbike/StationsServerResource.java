package fr.openbike;

import java.util.List;

import javax.jdo.PersistenceManager;

import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

	/**
	 * The server side implementation of the Restlet resource.
	 */
	public class StationsServerResource extends ServerResource {
	 
		@Get("json")
	    public List<Station> retrieve() {
	    	PersistenceManager pm = PMF.get().getPersistenceManager();
	        String query = "select from " + Station.class.getName();
	        List<Station> stations;
	        try {
	        	stations = (List<Station>) pm.newQuery(query).execute();
	        	pm.makeTransientAll(stations);
	        } finally{
	        	pm.close();
	        }
	        return stations;
	    }
}
