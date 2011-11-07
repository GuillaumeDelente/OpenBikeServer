from models import Station
from models import Network
from google.appengine.api import taskqueue, urlfetch, mail, users, app_identity
from django.http import HttpResponse
from BeautifulSoup import BeautifulStoneSoup
import re, math, logging, os

def update(request):
	count = Station.objects.count()
	if count == 0:
		fetchListHelper()
	else:
		to = int(math.floor(count / 10)) + 1
		update_url = Network.objects.get().update_url
		for i in range(0, to):
			taskqueue.add(queue_name='fetchStationsQueue', 
				      url='/private/fetchStations', 
				      params={'from': i, 'update_url': update_url}, 
				      method='POST')
	return HttpResponse('OK')

def fetchListHelper():
	network = Network.objects.get()
	taskqueue.add(queue_name='fetchListQueue', 
		      url='/private/fetchStationList', 
		      params={'url': network.list_url, 'id': network.id})

def fetchList(request):
	fetchListHelper()
	return HttpResponse('ok')

def fetchStationList(request):
	url = request.POST['url']
	network_id = request.POST['id']
	result = urlfetch.fetch(url)
	if result.status_code != 200:
		logging.error(
			'Unable to reach list webservice, error '
			+ str(result.result_code))
		return HttpResponseServerError(
			'Webservice error : ' 
			+ str(result.result_code))
	soup = BeautifulStoneSoup(result.content)
	old_ids = set(Station.objects.values_list('id', flat = True))
	new_ids = []
	need_slave_update = False
	#inserting
	for marker in soup.markers.findAll('marker'):
		new_id = int(marker['id'])
		new_ids.append(new_id)
		if new_id not in old_ids:
			need_slave_update = True
			Station(availableBikes = 0, 
				freeSlots = 0, 
				network = network_id, 
				name = marker['name'], 
				id = new_id,
				longitude = marker['lng'], 
				latitude = marker['lat'], 
				open = True, 
				payment = False, 
				special = False).save()
	#deleting
	for delete_id in old_ids.difference(set(new_ids)):
		need_slave_update = True
		Station.objects.get(id = delete_id).delete()

	#increment data version
	network = Network.objects.get()
#	network.data_version = F('data_version') + 1
	network.data_version += 1
	network.save()
	return HttpResponse('OK')

def fetchStations(request):

	def handle_result(rpc, i):
		result = rpc.get_result()
		if result.status_code == 200:
			update_station(stations[i], result.content)
		elif result.status_code == 403:
			mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
			to="contact@openbike.fr",
            subject="Access denied",
            body="Access denied for app " + get_application_id())
		else:
			logging.error('Unable to reach webservice ' 
				      + str(result.status_code) 
				      + ' for content : ' 
				      + result.content 
				      + ' for station ' 
				      + str(stations[i].id))

	# Use a helper function to define the scope of the callback.
	def create_callback(rpc, i):
		return lambda: handle_result(rpc, i)

	def update_station(station, content):
		soup = BeautifulStoneSoup(content)
		try:
			parsed_station = soup.station
			station.availableBikes = int(parsed_station.bikes.string)
			station.freeSlots = int(parsed_station.attachs.string)
			station.payment = parsed_station.paiement.string == 'AVEC_TPE'
			if len(station.address) == 0:
				station.address = parsed_station.adress.string.title()
			station.open = parsed_station.status.string == '0'
			station.save()
		except:
			mail.send_mail("bug@" + app_identity.get_application_id() + ".appspotmail.com",
			to="contact@openbike.fr",
			subject="Parsing Error",
			body='Error while parsing ' + str(station.id) + ' with content ' + content)

	url = request.POST['update_url']
	result_from = int(request.POST['from'])
	from_index = result_from * 10
	stations = Station.objects.all()[from_index:from_index + 10]
	rpcs = []
	for (i, station) in enumerate(stations):
		rpc = urlfetch.create_rpc()
		rpc.callback = create_callback(rpc, i)
		urlfetch.make_fetch_call(rpc, url + str(station.id))
		rpcs.append(rpc)

	for rpc in rpcs:
		rpc.wait()
	return HttpResponse('OK')
