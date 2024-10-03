import requests
import json
import random

URL = 'https://gottagofast.challenges.cfd'
def createUser(username, password, page):
    return requests.put(URL+'/users', json={'username':username,
                                            'password': password,
                                            'page': page})

# 	query := bson.M{"username": username}
def login(username, password):
    return requests.post(URL+'/users/login', json={'username': username,
                                                   'password': password},
                         )

def getPage(username, token = 'null'):
    return requests.get(URL+f'/users/page/{username}', 
                        headers={
                            'X-AUTH-TOKEN': token
                             })


"""
func (s *SessionServiceImpl) GetSession(ctx context.Context, token string) (models.Session, error) {
	var session models.Session
	query := bson.M{"token": token}

"""

user = '929295'
password = 'qwe123'
r = createUser(user,password,'https://www.yahoo.co.jp/')
# r = login(user,password)
# token = json.loads(r.content.decode())['X-AUTH-TOKEN']
# r = getPage('sonic', token)
# print(r.content.decode())
