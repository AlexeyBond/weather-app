from flask import *
import pymongo

import yawparser

import datetime
import traceback

DB_URI =	'mongodb://localhost:27017/'
DB_NAME =	'weatherapp_db'

WEATHER_UPDATE_PERIOD = datetime.timedelta(minutes=10)

db_client = pymongo.MongoClient(DB_URI)
db = db_client[DB_NAME]

app = Flask(__name__)

@app.errorhandler(500)
def page_not_found(e):
	print "\n\n",traceback.format_exc(),"\n\n"
	return 'Internal server error', 500

@app.route('/api/v0/weather',methods=['GET'])
def weather():
	city_id = request.args.get('city_id',None)

	if city_id == None:
		abort(418)

	city_id = int(city_id)

	weather_state = None
	weather_state_old = None

	weather = db.weather_cache.find_one({'city_id':city_id})

	if weather == None:
		weather = {'city_id':city_id}
	elif 'updated' in weather:
		if (datetime.datetime.now() - weather['updated']) < WEATHER_UPDATE_PERIOD:
			weather_state = weather.get('state',None)
		else:
			weather_state_old = weather.get('state',None)

	if weather_state == None:
		
		print '--- Downloading weather info for city',str(city_id),'...'

		weather_state = yawparser.parse_weather_info(city_id=city_id)
		if weather_state == None:
			if weather_state_old != None:
				weather_state = weather_state_old
				weather_state['outOfDate'] = True
			else:
				abort(404)
		else:
			weather['updated'] = datetime.datetime.now()
			weather['state'] = weather_state
			db.weather_cache.save(weather)

	return jsonify(weather_state)

if __name__ == '__main__':
	app.run( )
