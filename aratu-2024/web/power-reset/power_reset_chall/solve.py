import requests

r = requests.post('https://power-reset-281l3hof8xb646ls.boita.tech/reset_password', data={"password":"qwe123", 'confirm_password':'qwe123', 'id':'3cc8a74c-2f69-4d85-a2eb-1a9717a607d8' })

print(r.content.decode())
