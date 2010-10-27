package com.vcubserver;

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

/**
 * @author guitou
 *
 */
/**
 * @author guitou
 *
 */
public class UpdateVcub extends HttpServlet {

	/**
	 * Retrieve the whole list of Vcub Stations from the web.
	 */
	private static final long serialVersionUID = -1457525909708913828L;
	String NETWORK = "Vcub";

	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException, ServletException {
		/*
		 * Pattern p =Pattern.compile(
		 * "'latitude': '([^']*)', 'longitude': '([^']*)'[^#]*#(\\d*) - ([^<]*)</div>[^<]*<div class='gmap-adresse'>([^<]*)</div>(<div class='gmap-velos'>.*?<strong>(\\d+)</strong>.*?<strong>(\\d+)</strong>)?"
		 * ); Matcher m =p.matcher(
		 * "{ 'latitude': '44.84377', 'longitude': '-0.55751', 'text': '<div class='gmap-popup'><div class='gmap-infobulle'> <div class='gmap-titre'>#67 - Allee de Serr - Abadie</div> <div class='gmap-adresse'>ALLÉE DE SERR</div><div class='gmap-velos'> <table><tr> <td class='ok'><strong>12</strong> vélos disponibles</td> <td class='ok'><strong>6</strong> places disponibles</td></tr></table></div><div class='gmap-datemaj'>dernière mise à jour il y a <strong>00 min</strong> </div> </div></div>', 'markername': 'vcub' },"
		 * ); m.find(); System.out.println(m.group(8));
		 */
		long startTime = System.currentTimeMillis();
		process(req, resp);
		long endTime = System.currentTimeMillis();
		PersistenceManager pm = PMF.get().getPersistenceManager();
		long t = (endTime - startTime);
		pm.makePersistent(new Benchmark(t, "parse"));
		pm.close();
		resp.getWriter().println("Temps d'execution regexp : " + t);
	}

	public void process(HttpServletRequest req, HttpServletResponse resp)
			throws IOException, ServletException {
		StringBuilder result = new StringBuilder();
		// Send a GET request to the page
		try {
			// Send data
			URL url = new URL("http://www.vcub.fr/stations/plan");
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
			}
			// Get response
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					conn.getInputStream(), "UTF8"));
			while ((line = reader.readLine()) != null) {
				result.append(line);
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		int i = parseSlotsOnly(result.toString());
		// String a = parseStations(result);
		resp.setContentType("text/plain");
		resp.getWriter().println(
				"La mise à jour de " + i
						+ " stations à été correctement effectuée !");
		// resp.getWriter().println(a);
	}

	public static String sendGetRequest() {
		StringBuilder result = new StringBuilder();
		// Send a GET request to the servlet
		try {

			// Send data
			URL url = new URL("http://www.vcub.fr/stations/plan");

			// Get response
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					url.openStream(), "UTF8"));
			String line;

			while ((line = reader.readLine()) != null) {
				result.append(line);
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return result.toString();
	}

	/**
	 * Update Stations in Db, we just care about slots count
	 * 
	 * @param toParse : String to be parsed
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
		
		/* Retrieve our Stations from DB into a HashTable */
		PersistenceManager pm = PMF.get().getPersistenceManager();
		Extent<Station> extent = pm.getExtent(Station.class);
		Hashtable<Long, Station> stations = new Hashtable<Long, Station>(139);
		Iterator<Station> it = extent.iterator();
		if (it.hasNext()) {
			while (it.hasNext()) {
				Station s = it.next();
				stations.put(s.getId(), s);
			}
		} else {
			/* Our db is empty, let's fill it*/
			extent.closeAll();
			pm.close();
			return parseAllStations(toParse);
		}

		//System.out.println(toParse);
		p = Pattern
				.compile("#(\\d+)[^}]*(?:(?:<strong>(\\d+)</strong>[^}]*<strong>(\\d+)</strong>)|maintenance)");
		m = p.matcher(toParse);
		while (m.find()) {
			// System.out.println("Group : " + m.group(1) + " " + m.group(2) +
			// " " + m.group(3));
			Station s = stations.get(Long.parseLong(m.group(1)));
			if (s == null) {
				/* Vcub Station List has changed, we
				 * reload the whole list */
				extent.closeAll();
				pm.close();
				return parseAllStations(toParse);
			}
			if (m.group(2) != null) {
				s.setAvailableBikes(Integer.parseInt(m.group(2)));
				s.setFreeSlots(Integer.parseInt(m.group(3)));
				s.setOpen(true);
			} else {
				s.setOpen(false);
			}
		}
		extent.closeAll();
		pm.close();
		return stations.size();
	}
	
	public static int parseAllStations(String toParse) {

		Pattern p = Pattern.compile("'latitude': '([^']*)', 'longitude': '([^']*)'[^#]*#(\\d*) - ([^<]*)</div>[^<]*<div class='gmap-adresse'>([^<]*)</div>(<div class='gmap-velos'>.*?<strong>(\\d+)</strong>.*?<strong>(\\d+)</strong>)?");
		Matcher m = p.matcher(toParse);
		//FIXME : Size of the Vector
		Vector<Station> stations = new Vector<Station>(139);
		while (m.find()) {
			//System.out.println("Count -> " + m.groupCount());
			Station s = new Station();
			s.setNetwork("Vcub");
			s.setId(Long.parseLong(m.group(3)));
			s.setName(m.group(4));
			s.setAddress(m.group(5).toLowerCase());
			s.setLatitude(Double.parseDouble(m.group(1)));
			s.setLongitude(Double.parseDouble(m.group(2)));
			if (m.group(7) != null) {
				s.setAvailableBikes(Integer.parseInt(m.group(7)));
				s.setFreeSlots(Integer.parseInt(m.group(8)));
				s.setOpen(true);
			} else {
				s.setOpen(false);
			}
			stations.add(s);
		}
		PersistenceManager pm = PMF.get().getPersistenceManager();
		pm.makePersistentAll(stations);
		pm.close();
		return stations.size();
	}
}
