package fr.openbike;

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
public class Station {
	@PrimaryKey
	@Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
	private Long id;
	@Persistent
	private String network;
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
	boolean isOpen;
	@Persistent
	boolean isPayment;

	Station(long id, String network, String name, String address, 
			double longitude, double latitude, int availablesBikes, 
			int freeLocations, boolean isOpen, boolean hasPayment) {
		this.id = (long) id;
		this.network = network;
		this.address = address;
		this.name = name;
		this.longitude = longitude;
		this.latitude = latitude;
		this.availableBikes = availablesBikes;
		this.freeSlots = freeLocations;
		this.isOpen = isOpen;
		this.isPayment = hasPayment;
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
			setPayment(false);
		}
		
	}
	
	public String getNetwork() {
		return network;
	}

	public void setNetwork(String network) {
		this.network = network;
	}
	
	public void setId(long id) {
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
}