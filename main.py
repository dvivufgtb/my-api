import os
os.system('pip install flask')
import flask
from threading import Thread
import re
import random
import json
import base64

app = flask.Flask('')




@app.route('/regex', methods=['POST'])
def regex():
  regex = flask.request.get_json()['regex']
  text = flask.request.get_json()['text']
  return re.findall(regex, text)


@app.route('/random', methods=['POST'])
def random_():
  random1 = flask.request.get_json()['choices']
  random2 = int(flask.request.get_json()['amount'])
  responsetext = ''.join(random.choice(random1) for i in range(random2))
  return {'result': responsetext}


@app.route('/text/<manyak>', methods=['GET', 'PUT'])
def text(manyak):
  if flask.request.method == 'PUT':
    _text = flask.request.get_json()['text']
    _file = f'documents/{manyak}'
    if not _text:
      return "No text provided", 403
    else:
      if os.path.exists(_file):
        return "the name is already taken", 409
      else:
        with open(_file, 'w') as f:
          f.write(_text)
          return {"url": flask.request.url}, 201
  elif flask.request.method == 'GET':
    _file = f'documents/{manyak}'
    if not os.path.exists(_file):
      return "No text found", 404
    else:
      with open(_file, 'r') as f:
        return f.read()


@app.route('/base64', methods=['POST'])
def _base64():
  encode = flask.request.args.get('encode')
  value = flask.request.get_json(force=True)['value']
  if encode == 'true':
      try:
        converted = base64.b64encode(value.encode()).decode()
        return converted
      except Exception as e:
        return str(e), 400
  if encode == 'false':
    try:
      converted = base64.b64decode(value.encode()).decode()
      return converted
    except Exception as e:
      return str(e), 400
  else:
    return "encode argument must be true or false", 400

@app.route('/')
def home():
  return open('text.html', 'r').read()
  
def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  while True:
    t = Thread(target=run)
    t.start()
    t.join()


keep_alive()
