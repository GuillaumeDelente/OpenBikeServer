package com.vcubserver;

import javax.jdo.PersistenceManager;

import org.restlet.data.Status;
import org.restlet.resource.Get;
import org.restlet.resource.ResourceException;
import org.restlet.resource.ServerResource;

/**
 * The server side implementation of the Restlet resource.
 */
public class StationServerResource extends ServerResource {

	@Get("json")
	public Station toJson() throws ResourceException {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Station station;
		try {
			station = pm.getObjectById(Station.class,
					Long.parseLong(getRequestAttributes().get("station")
							.toString()));
		} catch (Exception e) {
			String msg = "Cannot get JSON representation";
			throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg, e);
		}
		
		finally {
			pm.close();
		}
		return station;
	}
/*
	@Get("xml")
	public Representation toXml() {
		String msg = "XML representation is not supported";
		throw new ResourceException(Status.SERVER_ERROR_INTERNAL, msg);
	}
	*/
}
