import requests
from tqdm import tqdm

"""
("INSERT INTO payloads (user_id, payload) VALUES (%s, %s)", $_SESSION['user'], $value));
"""

s = requests.Session()

URL = 'https://is-bypassable-yld7nbnacwlj72lk.boita.tech/'
# URL = 'http://localhost:3000/'

for i in range(1000):
    r = requests.post(URL, data={'value': '0x'+i*'F'})
    print(r.text)
