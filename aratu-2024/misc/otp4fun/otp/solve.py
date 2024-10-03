from pwn import *
import requests

p = process('./main')

s = []

for i in range(6):
    a = p.recvline().decode().strip()
    print(a)
    s.append(a)

print(s)

r = requests.post('https://otp4fun-cn4iteh1lslm9u2z.boita.tech/api/secrets', json={
    'secrets': s
    })

print(r.text)
