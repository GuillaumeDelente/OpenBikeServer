package fr.openbike.servlet;

import javax.jdo.PersistenceManager;

import org.restlet.data.Form;
import org.restlet.data.MediaType;
import org.restlet.data.Status;
import org.restlet.representation.Representation;
import org.restlet.representation.StringRepresentation;
import org.restlet.resource.Post;
import org.restlet.resource.ServerResource;

import fr.openbike.PMF;
import fr.openbike.object.Network;

public class NewNetwork extends ServerResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = -526191736230044015L;

	@Post
	public Representation acceptItem(Representation entity) {

		Form form = new Form(entity);
		Long id = Long.parseLong(form.getFirstValue("id"));
		String name = form.getFirstValue("name");
		String city = form.getFirstValue("city");
		String server = form.getFirstValue("server");
		String specialName = form.getFirstValue("specialName");
		Double longitude = Double.valueOf(form.getFirstValue("longitude"));
		Double latitude = Double.valueOf(form.getFirstValue("latitude"));

		if (name != null && city != null && longitude != null && specialName != null
				&& latitude != null && server != null) {
			PersistenceManager pm = PMF.get().getPersistenceManager();
			// The Query interface assembles a query
			pm.makePersistent(new Network(id, name, city, specialName, longitude, latitude, server));
			pm.close();
			setStatus(Status.SUCCESS_CREATED);
			return new StringRepresentation("Network inserted",
					MediaType.TEXT_PLAIN);
		}

		setStatus(Status.CLIENT_ERROR_NOT_FOUND);
		return new StringRepresentation("Network not inserted",
				MediaType.TEXT_PLAIN);
	}
}