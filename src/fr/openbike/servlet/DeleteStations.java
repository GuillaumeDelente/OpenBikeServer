package fr.openbike.servlet;

import java.io.IOException;
import java.util.List;

import javax.jdo.PersistenceManager;

import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Station;

public class DeleteStations extends ServerResource {
	
	@Get
	public void execute()
			throws IOException {
		System.out.println("Delete");
		PersistenceManager pm = PMF.get().getPersistenceManager();
	    String query = "SELECT FROM " + Station.class.getName();
	    List<Long> result = (List<Long>) pm.newQuery(query).execute();
	    pm.deletePersistentAll(result);
	    pm.close();
	}
}
