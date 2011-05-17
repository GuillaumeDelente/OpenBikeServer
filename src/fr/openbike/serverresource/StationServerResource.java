package fr.openbike.serverresource;

import javax.jdo.PersistenceManager;

import org.restlet.data.Status;
import org.restlet.resource.Get;
import org.restlet.resource.ResourceException;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Station;

/**
 * The server side implementation of the Restlet resource.
 */
public class StationServerResource extends ServerResource {

	@Get("json")
	public Station[] toJson() throws ResourceException {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		String[] station_ids_str = getRequestAttributes().get("station").toString().split("\\+");
		int size = station_ids_str.length;
		Station[] stations = new Station[size];
		try {
			for (int i = 0; i < size; i++) {
				stations[i] = pm.getObjectById(Station.class,
						Long.parseLong(station_ids_str[i]));
			}
		} catch (Exception e) {
			String msg = "Cannot get JSON representation";
			throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg, e);
		}
		
		finally {
			pm.close();
		}
		return stations;
	}
/*
	@Get("xml")
	public Representation toXml() {
		String msg = "XML representation is not supported";
		throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg);
	}
	*/
}
