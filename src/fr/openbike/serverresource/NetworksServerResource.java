package fr.openbike.serverresource;

import java.util.List;

import javax.jdo.PersistenceManager;
import javax.jdo.Query;

import org.restlet.data.Status;
import org.restlet.resource.Get;
import org.restlet.resource.ResourceException;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Network;


/**
 * The server side implementation of the Restlet resource.
 */
public class NetworksServerResource extends ServerResource {

	@Get("json")
	public List<Network> toJson() throws ResourceException {
		List<Network> results = null;
		PersistenceManager pm = PMF.get().getPersistenceManager();
		try {
			Query query = pm.newQuery(Network.class);
			results = (List<Network>) query.execute();
			pm.makeTransientAll(results);
		} catch (Exception e) {
			String msg = "Cannot get JSON representation";
			throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg, e);
		}
		
		finally {
			pm.close();
		}
		return results;
	}
/*
	@Get("xml")
	public Representation toXml() {
		String msg = "XML representation is not supported";
		throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg);
	}
	*/
}
