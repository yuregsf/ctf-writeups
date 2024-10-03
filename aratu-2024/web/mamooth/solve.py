from base64 import b64decode, b64encode
import requests
from tqdm import tqdm

token = "3TzixWQn/4AJvy8h44gIzso2Sl2KZd/LQpGtv5gY8oM="

def bitFlip( pos, bit, data):
    raw = b64decode(data)
    list1 = list(raw)
    list1[pos] = list1[pos] ^ bit
    raw = bytes(list1)
    return b64encode(bytes(raw)).decode()

for i in tqdm(range(32)):
    for j in tqdm(range(8)):
        new_token = bitFlip(i, j, token)
        r = requests.get('https://mamooth-0dlttfzipb38bewi.boita.tech', cookies={
            'auth': new_token,
            'INGRESSCOOKIE': '1727495242.795.8915.323105|b1d2891a899b25800736c58243c56450',
            'PHPSESSID': 'c45afa48bfcd0abf3b0bdf2b92f0c76a'
            })
        content = r.content.decode()
        if 'Enter password' in content or 'become an admin' in content: continue
        print(content)

