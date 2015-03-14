from flask import *
import pymongo
import bson
import json

import yawparser

import datetime
import traceback

import uuid

from functools import wraps

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

### Main part of API

@app.route('/api/v0/weather',methods=['GET'])
def weather1():
	city_id = request.args.get('city_id',None)
	return weather(city_id=city_id)

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

@app.route('/api/v0/cloth/items/<int:item_id>',methods=['GET'])
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
		cond_ok = cond_ok and (float(value) >= float(cond['from']))

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
		if v['weight'] > 0.01:
			choosen += [v.get('description',{'error':'Achtung! Invalid recird in DB.'})]

	print '>>>> ',str(choosen)

	return jsonify({'choise':choosen})

### API Calls for debugging/administration

def get_collection_scheme(collection,version='v0'):
	meta = db[collection+'.meta'].find_one({'version':version})
	schema = meta['schema']
	schema['$schema'] = meta['metaschema']
	return schema

def requiresAuthentication(view):
	@wraps(view)
	def wrapper(*args,**kwargs):
		cookie = request.cookies.get('session_id','')
		if db.sessions.find_one({'session_id':cookie}) == None:
			abort(401)
		return view(*args,**kwargs)
	return wrapper

def new_session(username):
	session_id = str(uuid.uuid4())
	db.sessions.insert({
			'username':username,
			'session_id':session_id,
			'created':datetime.datetime.now()})
	return session_id

@app.route('/api/v0/login',methods=['POST'])
def login():
	ct = request.headers.get('Content-Type',None)
	if ct in ('application/x-www-form-urlencoded','multipart/form-data'):
		return login_form( )

	if ct == 'application/json':
		return login_json( )

	abort(400)

def login_form():
	username = request.form['login']
	password = request.form['password']
	redirect_to = request.form.get('from','/')
	resp = redirect(redirect_to)
	if db.users.find_one({'name':username,'password':password}) != None:
		resp.set_cookie('session_id',new_session(username))
	return resp

def login_json():
	data = request.get_json()
	username = data.get('username','')
	password = data.get('password','')

	if db.users.find_one({'name':username,'password':password}) != None:
		session_id = new_session(username)
		resp = jsonify({'status':'OK'})
		resp.set_cookie('session_id',session_id)
		return resp

	abort(401)

@app.route('/api/v0/logout',methods=['POST'])
@requiresAuthentication
def logout():
	db.sessions.remove({'session_id':request.cookies['session_id']})

	resp = redirect(request.form.get('from','/'))
	resp.set_cookie('session_id','',expires=0)

	return resp

@app.route('/api/v0/cloth/items',methods=['POST'])
def cloth_post_new():
	return cloth_postitem(None)

@app.route('/api/v0/cloth/items.schema',methods=['GET'])
def cloth_item_schema():
	return jsonify(get_collection_scheme('cloth_items'))

@app.route('/api/v0/cloth/items/<item_id>',methods=['POST'])
@requiresAuthentication
def cloth_postitem(item_id=None):
	postitem = {'description':{}}

	if item_id != None:
		postitem['_id'] = bson.ObjectId(item_id)

	postitem['description']['name'] = request.form['description.name']
	postitem['description']['description'] = request.form['description.description']
	postitem['description']['group'] = request.form['description.group']
	postitem['description']['img'] = request.form['description.img']
	postitem['conditions'] = json.loads(request.form['conditions'])
	db.cloth_items.save(postitem)
	if request_wants_json():
		return jsonify({'status':'OK'})
	else:
		return redirect(request.form.get('from','/'))

@app.route('/api/v0/cloth/items/<item_id>',methods=['DELETE'])
@requiresAuthentication
def cloth_delitem(item_id):
	_id = bson.ObjectId(item_id)
	res = db.cloth_items.remove({'_id':_id})
	if res.get('n',0) == 0:
		abort(404)
	return jsonify({'status':'OK'})

@app.route('/api/v0/weather',methods=['POST'])
def weathercache_post_new():
	return weathercache_post(int(request.form['city_id']))

@app.route('/api/v0/weather/<int:city_id>',methods=['POST'])
@requiresAuthentication
def weathercache_post(city_id=0):
	postrecord={'state':{}}
	postrecord['city_id'] = city_id
	postrecord['updated'] = datetime.datetime.strptime(request.form['updated'],"%a, %d %b %Y %H:%M:%S +0000")
	postrecord['state']['temperature'] = float(request.form['state.temperature'])
	postrecord['state']['windVelocity'] = float(request.form['state.windVelocity'])
	postrecord['state']['windDirection'] = request.form['state.windDirection']
	postrecord['state']['weatherInWords'] = request.form['state.weatherInWords']
	postrecord['state']['humidity'] = float(request.form['state.humidity'])
	postrecord['state']['weatherThumbnailURL'] = request.form['state.weatherThumbnailURL']

	exist_record = db.weather_cache.find_one({'city_id':city_id})
	if exist_record != None:
		postrecord['_id'] = exist_record['_id']

	db.weather_cache.save(postrecord)
	if request_wants_json():
		return jsonify({'status':'OK'})
	else:
		return redirect(request.form.get('from','/'))


@app.route('/api/v0/cloth/items',methods=['GET'])
@requiresAuthentication
def cloth_getitems():
	query = {}

	if 'inname' in request.args:
		query['description.name'] = {'$regex':'.*'+request.args['inname']+'.*','$options':'i'}

	if 'group' in request.args:
		query['description.group'] = request.args['group']

	if 'indesc' in request.args:
		query['description.description'] = {'$regex':'.*'+request.args['indesc']+'.*','$options':'i'}

	qres = db.cloth_items.find(query)

	if 'orderby' in request.args:
		orderby = request.args['orderby']
		if orderby == 'name':
			qres = qres.sort([('description.name',1)])
		elif orderby == 'group':
			qres = qres.sort([('description.group',1)])
		else:
			abort(400)

	if 'page' in request.args:
		try:
			page = int(request.args['page'])

			if page < 1:
				page = 1

			count = int(request.args.get('count',10))

			if count <= 0:
				count = 10

			qres = qres.skip(count*(page-1)).limit(count)
		except:
			abort(400)

	items = list(qres)
	for item in items:
		item['_id'] = str(item['_id'])
	return jsonify({'items':items})

@app.route('/api/v0/weather/cached',methods=['GET'])
@requiresAuthentication
def weathercache_get():
	records = list(db.weather_cache.find())
	for rec in records:
		del rec['_id']
		rec['updated'] = rec['updated'].strftime("%a, %d %b %Y %H:%M:%S +0000")
	return jsonify({'records':records})



if __name__ == '__main__':
	app.run( )
