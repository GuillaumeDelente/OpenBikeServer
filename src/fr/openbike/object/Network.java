package fr.openbike.object;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

/**
 * Model class which will store the Station Items
 * 
 * @author Guillaume Delente
 *
 */
@PersistenceCapable
public class Network {
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long id;
	@Persistent
	private String name;
	@Persistent
	private String city;	
	@Persistent
	private String specialName;
	@Persistent
	private double longitude;
	@Persistent
	private double latitude;
	@Persistent
	private String server;

	public Network(long id, String name, String city, String specialName, double longitude, double latitude, String server) {
		this.id = id;
		this.name = name;
		this.city = city;
		this.specialName = specialName;
		this.longitude = longitude;
		this.latitude = latitude;
		this.server = server;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	public String getServer() {
		return server;
	}

	public void setServer(String server) {
		this.server = server;
	}
	
	public String getCity() {
		return city;
	}

	public void setCity(String city) {
		this.city = city;
	}
	
	public double getLongitude() {
		return longitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public double getLatitude() {
		return latitude;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public void setId(long id) {
		this.id = id;
	}

	public Long getId() {
		return id;
	}
	
	public String getSpecialName() {
		return specialName;
	}

	public void setSpecialName(String specialName) {
		this.specialName = specialName;
	}
}