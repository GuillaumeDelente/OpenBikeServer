package fr.openbike.servlet;

import java.io.IOException;
import java.util.List;

import javax.jdo.PersistenceManager;
import javax.jdo.Query;

import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Network;

public class DeleteNetworks extends ServerResource {
	
	@Get
	public void execute()
			throws IOException {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query q = pm.newQuery(Network.class);
	    List<Network> result = (List<Network>) q.execute();
	    pm.deletePersistentAll(result);
	    pm.close();
	}
}
