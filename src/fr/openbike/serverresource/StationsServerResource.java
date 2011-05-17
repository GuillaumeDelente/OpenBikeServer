package fr.openbike.serverresource;

import java.util.List;

import javax.jdo.PersistenceManager;
import javax.jdo.Query;

import org.restlet.resource.Get;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Station;

/**
 * The server side implementation of the Restlet resource.
 */
public class StationsServerResource extends ServerResource {

	@Get("json")
	public List<Station> retrieve() {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Query query = pm.newQuery(Station.class);
		int network = 0;
		query.setOrdering("id asc");
		if (getRequestAttributes() != null) {
			String networkStr = (String) getRequestAttributes().get("city");
			if (networkStr != null) {
				network = Integer.parseInt(networkStr);
				query.setFilter("network == networkParam");
				query.declareParameters("int networkParam");
			}
		}
		List<Station> stations;
		try {
			if (network == 0)
				stations = (List<Station>) query.execute(1);
			else
				stations = (List<Station>) query.execute(network);
			pm.makeTransientAll(stations);
		} finally {
			pm.close();
		}
		return stations;
	}
}
