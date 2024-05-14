import os
import traceback
import flask
from threading import Thread
import re
import random
import json
import base64
import datetime as dt
import requests,aiohttp
import html
from cryptography.fernet import Fernet
from requests.structures import CaseInsensitiveDict
from markdown import markdown
app = flask.Flask('')

def guess_ext(mime):
 mime_to_ext = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'text/plain': 'txt',
        'image/webp': 'webp',
        'application/json': 'json'
        # Add more mappings as needed
    }
 try: return '.'+mime_to_ext[mime]
 except: return ''
def is_json(my_str):
    try:
        json.loads(my_str)
    except ValueError:
        return False
    return True
@app.route('/regex', methods=['POST'])
def regex():
  
  regex = flask.request.get_json()['regex']
  text = flask.request.get_json()['text']
  r = re.compile(regex)
  matches = [
    {'content':m.group(),
     "startPos": m.start(),
     "endPos": m.end()} for m in r.finditer(text)
  ]
  return matches
  
  

@app.route('/split', methods=['POST'])
def split():
  splitter = flask.request.get_json(force=True)['sep']
  text: str = flask.request.get_json(force=True)['text']
  splitted = text.split(splitter)
  return splitted

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
    if re.search('[^A-Za-z0-9-_]', manyak):
       return "special characters are not allowed", 400
    _file = f'documents/{manyak}'
    if not _text:
      return "No text provided", 403
    else:
      if os.path.exists(_file):
        return "the name is already taken", 409
      else:
        with open(_file, 'wb') as f:
          f.write(_text.encode())
          return {"url": flask.request.url}, 201
  elif flask.request.method == 'GET':
    _file = f'documents/{manyak}'
    if not os.path.exists(_file):
      return "No text found", 404
    else:
      with open(_file, 'rb') as f:
        content = f.read()
        f.close()
      if is_json(content.decode()):
        content_type = 'application/json'
      else:
        content_type = 'text/plain'
      return flask.Response(content, content_type=f'{content_type}; charset=utf-8', status=302)
@app.route('/arraytolines', methods=['POST'])
def arraytolines():
  content = flask.request.get_json()['arrays']
  if isinstance(content, list):
     return '\n'.join(content), 202
  else:
    if not content:
      return {'arrays':'this field is required'}, 400
    else:
      return {'arrays':'must be a json array'}, 406

@app.route('/discord-permissions/<perms>')
def discordpermissions(perms):
  permissions = {
    'create_instant_invite': 0x1,
    'kick_members': 0x2,
    'ban_members': 0x4,
    'administrator': 0x8,
    'manage_channels': 0x10,
    'manage_guild': 0x20,
    'add_reactions': 0x40,
    'view_audit_log': 0x80,
    'priority_speaker': 0x100,
    'stream': 0x200,
    'read_messages': 0x400,
    'send_messages': 0x800,
    'send_tts_messages': 0x1000,
    'manage_messages': 0x2000,
    'embed_links': 0x4000,
    'attach_files': 0x8000,
    'read_message_history': 0x10000,
    'mention_everyone': 0x20000,
    'use_external_emojis': 0x40000,
    'view_guild_insights': 0x80000,
    'connect': 0x100000,
    'speak': 0x200000,
    'mute_members': 0x400000,
    'deafen_members': 0x800000,
    'move_members': 0x1000000,
    'use_vad': 0x2000000,
    'change_nickname': 0x4000000,
    'manage_nicknames': 0x8000000,
    'manage_roles': 0x10000000,
    'manage_webhooks': 0x20000000,
    'manage_emojis': 0x40000000,
    'use_application_commands': 0x80000000
}
  permission_names = []
  try:
   for name, value in permissions.items():
    if int(perms) & value:
      permission_names.append(name)

   return permission_names
  except: return html.escape(traceback.format_exc())


@app.route('/base64', methods=['POST'])
def _base64():
  encode = flask.request.args.get('encode')
  value = flask.request.get_json(force=True)['value']
  encode = 'true' if encode.lower() not in ['true','false'] else encode
  if encode.lower() == 'true':
      try:
        converted = base64.b64encode(value.encode()).decode()
        return converted
      except:
        return html.escape(traceback.format_exc()), 400
  if encode.lower() == 'false':
    try:
      converted = base64.b64decode(value.encode()).decode()
      return converted
    except:
      return html.escape(traceback.format_exc()), 400
@app.route('/isoformat/<unix>') 
def isoformat(unix):
    iso_format = dt.datetime.fromtimestamp(float(unix), dt.UTC).isoformat()
    response = {"iso": iso_format}
    try:
      strftime = flask.request.args['strftime']
      custom_iso = dt.datetime.fromtimestamp(float(unix), dt.UTC).strftime(strftime)
      
      response['custom_iso'] = custom_iso
    
    
    except: pass
    return response


@app.route('/discord-file', methods=['POST'])
async def discord_file():
    payload = flask.request.get_json()
    auth = flask.request.headers.get('Authorization')
    channel_id = flask.request.args.get('channel')
    payload_json = payload.get('payload_json', {})
    attachment_url: str = payload['attachment_url']
    att_url = attachment_url.split('?')[0]
    try:
      r = requests.get(attachment_url)
      r.raise_for_status()
      try:
        filename = payload['filename']
      except:
        wtf = att_url.split('/')
        wtf.reverse()
        filename = wtf[0]
      req_body = {
        filename:r.content,
        'payload_json':json.dumps(payload_json)}
      #resp = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers={'authorization':auth}, data={'payload_json':json.dumps(payload_json)}, files={'file':(filename, r.content)})
      async with aiohttp.ClientSession(headers={'authorization':auth}) as ses:
        async with ses.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', data=req_body) as res:
          resp = res
          _content = await resp.read()

      return flask.Response(_content, resp.status, content_type=resp.headers.get('content-type'))
    except:
      try:
       status_code = r.status_code
      except:
       status_code = 502
      return flask.Response(traceback.format_exc(), status_code, content_type='text/plain')

@app.route('/requests/<method>', methods=['POST'])
async def send_requests(method):
   try:
    get_json: dict = flask.request.get_json()
   except:
    get_json = {}
   try:
    url = flask.request.args.get('url')
    headers: dict = get_json.get('headers', {})
    payload = get_json.get('data', None)
   except:
     return flask.Response(traceback.format_exc(), 400, content_type='text/plain')
    
    
   
   try: 
    async with aiohttp.ClientSession(headers=headers) as session:
      async with session.request(method, url, data=payload) as response:

       try:resp = await response.json(encoding='utf-8')
       except:resp = await response.text(encoding='utf-8', errors='ignore')
       resp_headers = dict(response.headers)
       return {'response':resp, 'headers':resp_headers}, response.status
   except:
    return f'''
<div style="text-align: center; color: #345; padding-top: 10px;">
<p><strong><span style="color: #ff6600;">{html.escape(traceback.format_exc())}</span></strong></p>
</div>
''', 418
   
@app.route('/fernet/<option>', methods=['POST'])
def fernet(option):
 if option in ['generate','encrypt','decrypt']:
  if option == 'generate':
    return Fernet.generate_key()
  

  
  
  else:
    data = flask.request.get_json()
    try:
      
      fernet_key = data['fernet_key']

      _fernet_ = Fernet(fernet_key)

      if option == 'encrypt':
        text = _fernet_.encrypt(data['data'].encode())
      else:
        text = _fernet_.decrypt(data['data'])
      return flask.Response(text, content_type='text/plain; charset=utf-8')



    except:
      return flask.Response(traceback.format_exc(), 409, content_type='text/plain; charset=utf-8')

 else:
   
    return "the options must be one of these options: generate, encrypt, decrypt", 400
      
@app.route('/just-paste/<document>')
def idk(document):
  r = requests.get(f'https://just-paste.it/documents/{document}')
  try: return flask.Response(r.json()['text'], content_type='text/plain; charset=utf-8')
  except: return r.text, r.status_code

@app.route('/')
def home():
  return markdown(open('readme.md').read())
  
def run():
  app.run(host='0.0.0.0', port=random.randint(2024, 6969))


def keep_alive():
  while True:
    t = Thread(target=run)
    t.start()
    t.join()

if __name__ == '__main__':
 Thread(target=keep_alive).start()