package fr.openbike.object;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PrimaryKey;

import com.google.appengine.api.datastore.Key;

/**
 * Model class which will store the Station Items
 * 
 * @author Guillaume Delente
 *
 */
@PersistenceCapable
public class Station {
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long id;
	@Persistent
	private int network;
	@Persistent
	private String name;
	@Persistent
	private String address;
	@Persistent
	private double longitude;
	@Persistent
	private double latitude;
	@Persistent
	private int availableBikes;
	@Persistent
	private int freeSlots;
	@Persistent
	private boolean isOpen;
	@Persistent
	private boolean isPayment;	
	@Persistent
	private boolean isSpecial = false;

	Station(Long id, int network, String name, String address, 
			double longitude, double latitude, int availablesBikes, 
			int freeLocations, boolean isOpen, boolean hasPayment, boolean isSpecial) {
		this.id = id;
		this.network = network;
		this.address = address;
		this.name = name;
		this.longitude = longitude;
		this.latitude = latitude;
		this.availableBikes = availablesBikes;
		this.freeSlots = freeLocations;
		this.isOpen = isOpen;
		this.isPayment = hasPayment;
		this.isSpecial = isSpecial;
	}

	public Station() {
		// TODO Auto-generated constructor stub
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	public void setAddress(String address) {
		this.address = address;
	}

	public String getAddress() {
		return address;
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

	public int getAvailableBikes() {
		return availableBikes;
	}

	public void setAvailableBikes(int availablesBikes) {
		this.availableBikes = availablesBikes;
	}

	public int getFreeSlots() {
		return freeSlots;
	}

	public void setFreeSlots(int freeSlots) {
		this.freeSlots = freeSlots;
	}

	public boolean isOpen() {
		return isOpen;
	}

	public void setOpen(boolean isOpen) {
		if((this.isOpen = isOpen) == false) {
			setAvailableBikes(0);
			setFreeSlots(0);
		}
		
	}
	
	public int getNetwork() {
		return network;
	}

	public void setNetwork(int network) {
		this.network = network;
	}
	
	public void setId(Long id) {
		this.id = id;
	}

	public Long getId() {
		return id;
	}
	
	public boolean isPayment() {
		return isPayment;
	}
	
	public void setPayment(boolean payment) {
		this.isPayment = payment;
	}	
	
	public boolean isSpecial() {
		return isSpecial;
	}
	
	public void setSpecial(boolean isSpecial) {
		this.isSpecial = isSpecial;
	}
}