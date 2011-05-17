package fr.openbike.servlet;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.jdo.Extent;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import fr.openbike.PMF;
import fr.openbike.Utils;
import fr.openbike.object.Station;

/**
 * @author Guillaume Delente
 * 
 */
public class UpdateVcub extends HttpServlet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 6512458009254635494L;
	/**
	 * Retrieve the whole list of Vcub Stations from the web.
	 */
	private static final String URL = "http://www.vcub.fr/stations/plan";
	public static final int BORDEAUX = 1;

	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException, ServletException {
		StringBuilder result = new StringBuilder();
		// Send a GET request to the page
		try {
			// Send data
			URL url = new URL(URL);
			String line;
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn
					.setRequestProperty(
							"User-Agent",
							"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.41 Safari/534.7");
			conn.setConnectTimeout(5000);
			conn.setReadTimeout(5000);
			if (200 != conn.getResponseCode()) {
				System.out.println("Cannot connect to the website");
				conn.disconnect();
				return;
			}
			// Get response
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					conn.getInputStream(), "UTF8"));
			while ((line = reader.readLine()) != null) {
				result.append(line);
			}
			reader.close();
			parseSlotsOnly(result.toString());
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	/**
	 * Update Stations in Db, we just care about slots count
	 * 
	 * @param toParse
	 *            : String to be parsed
	 * @return the count of updated stations
	 */
	public static int parseSlotsOnly(String toParse) {
		/* Some cleaning in the String */
		Pattern p = Pattern.compile(".*\"markers\": \\[(.*?)\\].*");
		Matcher m = p.matcher(toParse);
		m.find();
		toParse = m.group(1);
		toParse = toParse.replaceAll("\\\\x3c", "<");
		toParse = toParse.replaceAll("\\\\x3e", ">");
		toParse = toParse.replaceAll("(\\\\')|(\\\\)?\"", "'");

		// return parseAllStations(toParse);

		// Retrieve our Stations from DB into a HashTable

		PersistenceManager pm = PMF.get().getPersistenceManager();

		Extent<Station> extent = pm.getExtent(Station.class);
		Hashtable<Long, Station> stations = new Hashtable<Long, Station>();
		Iterator<Station> it = extent.iterator();
		if (it.hasNext()) {
			while (it.hasNext()) {
				Station s = it.next();
				stations.put(s.getId(), s);
			}
		} else {
			// Our db is empty, let's fill it
			pm.close();
			// return toParse;
			return parseAllStations(toParse);
		}
		// System.out.println(toParse);
		p = Pattern
				.compile("#(\\d+)([^}]*<strong>(\\d+)</strong>[^}]*<strong>(\\d+)</strong>"
						+ "([^<]*</td><td><acronym title='Carte Bancaire'>CB</acronym></td>)?"
						+ ")?([^}]*'markername': 'vcub')?");
		m = p.matcher(toParse);
		while (m.find()) {
			// System.out.println("Group : " + m.group(1) + " " + m.group(2) +
			// " " + m.group(3));
			Station s = stations.get(Long.parseLong(m.group(1)));
			if (s == null) {
				// Vcub Station List has changed, we
				// reload the whole list
				pm.close();
				return parseAllStations(toParse);
			}
			if (m.group(2) != null) {
				s.setAvailableBikes(Integer.parseInt(m.group(3)));
				s.setFreeSlots(Integer.parseInt(m.group(4)));
				s.setOpen(true);
				s.setPayment(m.group(5) != null);
				s.setSpecial(m.group(6) == null);
			} else {
				s.setOpen(false);
			}
		}
		pm.close();
		return stations.size();
	}

	public static int parseAllStations(String toParse) {
		Pattern p = Pattern
				.compile("'latitude': '([^']*)', 'longitude': '([^']*)'[^#]*#(\\d*) - ([^<]*)</div>[^<]*<div class='gmap-adresse'>([^<]*)</div>"
						+ "(<div class='gmap-velos'>.*?<strong>(\\d+)</strong>.*?<strong>(\\d+)</strong>"
						+ "([^<]*</td><td><acronym title='Carte Bancaire'>CB</acronym></td>)?"
						+ ")?([^}]*'markername': 'vcub')?");
		Matcher m = p.matcher(toParse);
		Vector<Station> stations = new Vector<Station>();
		String a = "";
		while (m.find()) {
			Station s = new Station();
			s.setNetwork(BORDEAUX);
			s.setId(Long.parseLong(m.group(3)));
			// a += Long.parseLong(m.group(3));
			s.setName(Utils.capitalizeFully(m.group(4)));
			s.setAddress(Utils.capitalizeFully(m.group(5)));
			s.setLatitude(Double.parseDouble(m.group(1)));
			s.setLongitude(Double.parseDouble(m.group(2)));
			if (m.group(7) != null) {
				s.setAvailableBikes(Integer.parseInt(m.group(7)));
				s.setFreeSlots(Integer.parseInt(m.group(8)));
				s.setPayment(m.group(9) != null);
				s.setOpen(true);
				s.setSpecial(m.group(10) == null);
				a += m.group(10) + "\n ";
			} else {
				s.setOpen(false);
			}
			stations.add(s);
		}
		PersistenceManager pm = PMF.get().getPersistenceManager();
		pm.makePersistentAll(stations);
		pm.close();
		// return "Result : " + a;
		return stations.size();
	}
}
