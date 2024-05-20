from flask import Blueprint, request
import json
# Create a Blueprint object
json_route = Blueprint('json_route', __name__)

# Define a route
@json_route.route('/dict/<arg>', methods=['POST'])
def dictXD(arg):
   _json_ = request.get_json()
   try:
    if arg.lower() == 'get':
       _data_ = _json_.get('object')
       _key_ = _json_.get('key')
       _default_ = _json_.get('default')
       return _data_.get(_key_, _default_)
    elif arg.lower() == 'update':
       _data_ = _json_.get('object')
       _value_ = _json_.get('value', {})
       response = _data_
       response.update(_value_)
       return response
    elif arg.lower() == 'items':
       _data_ = _json_.get('object')
       return list(_data_.items()) 
    else: return ['get','update','items']
   except Exception as e: return str(e), 400


@json_route.route('/list/<arg>', methods=['POST'])
def listXD(arg):
   _json_ = request.get_json()
   try:
    if arg.lower() == 'extend':
      _data_ = _json_.get('object')
      _data_.extend(_json_.get('value', []))
      return _data_
    elif arg.lower() == 'reverse':
      _data_ = _json_.get('object')
      _data_.reverse()
      return _data_
    else: return ['extend','reverse']
   except Exception as e: return str(e), 400







@json_route.route('/json/<arg>', methods=['POST'])
def jsonXD(arg):
    _json_ = request.get_json()
    try: 
     if arg.lower() == 'parse':
       _data_ = _json_.get('string')
       return {'parsed':json.loads(_data_)}
     elif arg.lower() == 'stringify':
       _data_ = _json_.get('object')
       return {'string':json.dumps(_data_, indent=_json_.get('indent'))}
    except Exception as e: return str(e), 400