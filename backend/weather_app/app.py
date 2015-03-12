from flask import *
import pymongo
import bson
import json

import yawparser

import datetime
import traceback

DB_URI =	'mongodb://localhost:27017/'
DB_NAME =	'weatherapp_db'

WEATHER_UPDATE_PERIOD = datetime.timedelta(minutes=1)

db_client = pymongo.MongoClient(DB_URI)
db = db_client[DB_NAME]

app = Flask(__name__)

###

def request_wants_json():
	best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
	return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

### Error handlers

@app.errorhandler(500)
def page_not_found(e):
	print "\n\n",traceback.format_exc(),"\n\n"
	return 'Internal server error', 500

@app.route('/api/v0/weather',methods=['GET'])
def weather1():
	city_id = request.args.get('city_id',None)
	return weather(city_id=city_id)

### Main part of API

@app.route('/api/v0/weather/<int:city_id>',methods=['GET'])
def weather(city_id=None):

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

@app.route('/api/v0/cloth/item/<int:item_id>',methods=['GET'])
def cloth_getitem(item_id=0):
	item = db.cloth_items.find_one({'id':int(item_id)})

	if item == None:
		return Response('{}',mimetype='application/json',status=404)

	return jsonify(item.get('description',{}))

def check_item_condition(cond,context):
	value = context.get(cond.get('value',''),'0')
	cond_ok = True

	if 'is' in cond:
		cond_ok = cond_ok and (str(value) == cond['is'])

	if 'from' in cond:
		cond_ok = cond_ok and (float(value) > float(cond['from']))

	if 'to' in cond:
		cond_ok = cond_ok and (float(value) < float(cond['to']))

	return cond_ok

def calc_item_weight(item,context):
	conditions = item.get('conditions',[])

	weight = 0.0

	for cond in conditions:
		weight += cond.get('weight',0.0) * (1.0 if check_item_condition(cond,context) else 0.0)

	return weight

@app.route('/api/v0/cloth/choose',methods=['GET'])
def cloth_choose():
	context = {}
	context['temperature'] = float(request.args.get('temperature',0))
	context['windVelocity'] = float(request.args.get('windVelocity',0))
	context['season'] = request.args.get('season','')

	itemgroups = {}

	for item in db.cloth_items.find():
		item = dict(item)
		del item['_id']
		group = item.get('description',{}).get('group','')
		weight = calc_item_weight(item,context)
		item['weight'] = weight
		if group not in itemgroups:
			itemgroups[group] = item
		else:
			weight = calc_item_weight(item,context)
			if itemgroups[group]['weight'] < weight:
				itemgroups[group] = item

	choosen = []

	for k, v in itemgroups.items():
		choosen += [int(v.get('id',0))]

	print '>>>> ',str(choosen)

	return jsonify({'choise':choosen})

### API Calls for debugging/administration

@app.route('/api/v0/cloth/item/<int:item_id>',methods=['POST'])
def cloth_postitem(item_id=0):
	postitem = {'description':{}}
	postitem['description']['name'] = request.form['description.name']
	postitem['description']['description'] = request.form['description.description']
	postitem['description']['group'] = request.form['description.group']
	postitem['description']['img'] = request.form['description.img']
	postitem['id'] = int(request.form['id'])
	postitem['_id'] = bson.ObjectId(request.form['_id'])
	postitem['conditions'] = json.loads(request.form['conditions'])
	db.cloth_items.save(postitem)
	if request_wants_json():
		return jsonify({'status':'OK'})
	else:
		return redirect('/frontend/admin.html')

@app.route('/api/v0/weather/<int:city_id>',methods=['POST'])
def weathercache_post(city_id=0):
	postrecord={'state':{}}
	postrecord['city_id'] = int(request.form['id'])
	postrecord['_id'] = bson.ObjectId(request.form['_id'])
	postrecord['updated'] = datetime.strptime(request.form['updated'],"%a, %d %b %Y %H:%M:%S +0000")
	postrecord['state']['temperature'] = float(request.form['state.temperature'])
	postrecord['state']['windVelocity'] = float(request.form['state.windVelocity'])
	postrecord['state']['windDirection'] = request.form['state.windDirection']
	postrecord['state']['weatherInWords'] = request.form['state.weatherInWords']
	postrecord['state']['humidity'] = float(request.form['state.humidity'])
	postrecord['state']['weatherThumbnailURL'] = request.form['state.weatherThumbnailURL']
	db.weather_cache.save(postrecord)
	if request_wants_json():
		return jsonify({'status':'OK'})
	else:
		return redirect('/frontend/admin.html')


@app.route('/api/v0/cloth/items',methods=['GET'])
def cloth_getitems():
	items = list(db.cloth_items.find())
	for item in items:
		item['_id'] = str(item['_id'])
	return jsonify({'items':items})

@app.route('/api/v0/weather/cached',methods=['GET'])
def weathercache_get():
	records = list(db.weather_cache.find())
	for rec in records:
		rec['_id'] = str(rec['_id'])
		rec['updated'] = rec['updated'].strftime("%a, %d %b %Y %H:%M:%S +0000")
	return jsonify({'records':records})



if __name__ == '__main__':
	app.run( )
