import requests, json, datetime
from bs4 import BeautifulSoup

class RenfeTime:
	"""
	Base class for RenfeTime
	Scrapes and parses RENFE's schedule webpage. 
	Only Asturias is supported at the moment
	"""

	BASE_URL = "http://horarios.renfe.com/cer/hjcer310.jsp?"
	STATIONS = {   
		'Ablaña': 15205,
		'Aviles': 16403,
		'Barros': 16006,
		'Calzada Asturias': 15401,
		'Campomanes': 15120,
		'Cancienes': 16302,
		'Ciaño': 16010,
		'El Caleyo': 15210,
		'El Entrego': 16011,
		'Ferroñes': 16301,
		'Gijón': 15410,
		'La Cobertoria': 15121,
		'La Corredoria': 15217,
		'La Felguera': 16008,
		'La Frecha': 15119,
		'La Pereda-Riosa': 15206,
		'La Rocica': 16402,
		'Las Segadas': 15209,
		'Llamaquique': 15218,
		'Los Campos': 16408,
		'Lugo de LLanera': 15300,
		'Lugones': 15212,
		'Mieres-Puente': 15203,
		'Monteana': 15303,
		'Nubledo': 16400,
		'Olloniego': 15207,
		'Oviedo': 15211,
		'Peña Rubia': 16005,
		'Pola de Lena': 15122,
		'Puente L.Fierros': 15118,
		'Sama': 16009,
		'San Juan de Nieva': 16405,
		'Santa Eulalia M.': 16001,
		'Santullano': 15202,
		'Serin': 15302,
		'Soto de Rey': 15208,
		'Tudela-Veguin': 16002,
		'Ujo': 15200,
		'Veriña': 15400,
		'Villabona Astur': 15301,
		'Villabona-Tabladiello': 15305,
		'Villalegre': 16401,
		'Villallana': 15123
	}

	@staticmethod
	def datetime_to_renfeDate(datetime_time):
		return "{:02}".format(datetime_time.year) +"{:02}".format(datetime_time.month) + "{:02}".format(datetime_time.day)

	@staticmethod
	def getTimeTable(origin, destination, date, from_time = "00", to_time = "26", as_json = False):
		"""
		getTimeTable accesses renfe.com schedule page and scrapes the 
		train timetable with the specified data

		Params:
			:param: origin      -> Code designating the origin station
			:param: destination -> Code designating the destination station
			:param: date        -> Date of travel (format: datetime.date())
			:param: from_time   -> Departure hour (increases one by one from 
								   05 to 23, the special hour 00 means "All")
			:param: to_time     -> Arrival hour (increases one by one from 05 
								   (meaning 05:59) to 23 (meaning 23:59), the 
								   special value 26 means "All")
			:param: as_json     -> Flag to determine if the schedule should be
								   returned as a json string
		Returns:
			:return: Nested dictionary with schedule data
		"""

		date = RenfeTime.datetime_to_renfeDate( date )

		total_timetable = {
			"origin_station" : origin,
			"destination_station" : destination,
			"date" : date,
			"from_hour" : from_time,
			"to_hour" : to_time,
			"events" : []
		}

		page_content = requests.post(f"{RenfeTime.BASE_URL}nucleo=20&i=s&cp=NO&o={origin}&d={destination}&df={date}&ho={from_time}&hd={to_time}&TXTInfo=").content
		soup = BeautifulSoup(page_content, 'html.parser')
		trains = soup.find_all("tr")

		for train_index in range(len(trains)):
			current_train_data = []

			train = trains[ train_index ]

			for field in train.find_all("td"):
				current_train_data.append(field.getText().strip())

			del current_train_data[1]

			line, departure_h, arrival_h, travel_t = current_train_data

			time_event = {
				"line" : line,
				"departure_hour" : departure_h,
				"arrival_hour" : arrival_h,
				"travel_time" : travel_t }

			total_timetable[ "events" ].append( time_event )
		
		return total_timetable
			
	@staticmethod
	def list_stations():
		"""
		Returns a list containing all known stations
		"""
		return [ i for i in RenfeTime.STATIONS.keys() ].sort()
	
	@staticmethod
	def getStationCode(location):
		try:
			return RenfeTime.STATIONS[ location ]
		except:
			raise Exception("The selected location does not exist, please, use list_stations() to get a list of all avalaible stations")