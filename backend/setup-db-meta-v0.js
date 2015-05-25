/*
 * Загружает в БД схему сущности "предмет одежды"
 */

var METADATA = {
	'cloth_items' : {
		'version': 'v0',
		'metaschema': 'http://json-schema.org/draft-04/schema',
		'schema': {
			'type': 'object',
			'properties': {
				'description': {
					'type': 'object',
					'properties': {
						'name': {
							'type': 'string'
						},
						'description': {
							'type': 'string'
						},
						'group': {
							'type': 'string'
						},
						'img': {
							'type': 'string'
						}
					},
					'required':['name','description','group','img']
				},
				'conditions': {
					'type': 'array',
					'items': {
						'type': 'object',
						'properties': {
							'variable': {
								'type': 'string'
							},
							'weight': {
								'type': 'number'
							},
							'from': {
								'type': 'number'
							},
							'to': {
								'type': 'number'
							},
							'is': {
								'type': ['string','number']
							}
						}
					},
					'required':['variable']
				},
				'_id':{/*'type': 'objectid'*/}
			},
			'required': ['description','conditions','_id']
		}
	}
}

/*****************************************************************************/
db = db.getSiblingDB('weatherapp_db')

for(var key in METADATA)
{
	if(METADATA.hasOwnProperty(key))
	{
		var val = METADATA[key];
		metacollection_name = key + '.' + 'meta';

		print('-->'+metacollection_name)

		metacollection = db[metacollection_name]

		metacollection.remove({'version':val.version})
		metacollection.insert(val)
	};
};
