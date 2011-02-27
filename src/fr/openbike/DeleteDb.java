package fr.openbike;

import java.io.IOException;
import java.util.List;

import javax.jdo.PersistenceManager;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@SuppressWarnings("serial")
public class DeleteDb extends HttpServlet {
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		PersistenceManager pm = PMF.get().getPersistenceManager();
	    String query = "SELECT FROM " + Station.class.getName();
	    List<Long> result = (List<Long>) pm.newQuery(query).execute();
	    pm.deletePersistentAll(result);
	    pm.close();
	}
}
