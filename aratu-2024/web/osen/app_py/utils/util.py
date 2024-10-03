import json, uuid

USERS = []
method = ['get', 'post']

class User:
    def __init__(self, name, age, username, role):
        self.name = name
        self.age = age
        self.username = username
        self.role = role
        self.uuid = str(uuid.uuid4())

    def serialize(self):
        len_users = len(USERS)

        USERS.append({
            'name': self.name,
            'age': self.age,
            'username': self.username,
            'role': self.role,
            'session_id': self.uuid
        })

        return self.uuid

def update_user(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                update_user(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            update_user(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

def get_user_session(session_id):
    for user in USERS:
        if user.get('session_id') == session_id:
            return user.get('username')
        else:
            return False

def check_url(session_id):
    for user in USERS:
        if user.get('username') == get_user_session(session_id) and user.get('url') and user.get('role') == 'admin':
            try:
                url = user.get('url')
                return url
            except:
                return False
        
def check_user_exists(username):
    for user in USERS:
        if user.get('username') == username:
            return True
        else:
            return False

def return_user_information(session_id):
    print(USERS)
    for user in USERS:
        if user.get('session_id') == session_id:
            return user
        else:
            return False
        
