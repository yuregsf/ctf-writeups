import requests, json
from flask import Flask, request, jsonify
from utils.util import User, update_user, USERS, check_url, check_user_exists, get_user_session, return_user_information
from functools import wraps

app = Flask(__name__)
method = ['get','post']

def require_session(require_session):
    @wraps(require_session)

    def check_session(*args, **kwargs):
        session = request.cookies.get('session_id')
        if session:
            return require_session(*args, **kwargs)
        else:
           return jsonify({'error': 'Missing session_id header'}), 403

    return check_session

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    age = data.get('age')

    if check_user_exists(username):
        return jsonify({'error': 'User already exists'})
    
    if not name or not username or not age:
        params = [name, username, age]
        
        for param in range(3):
            if params[param] == None:
               if param == 0:
                  return jsonify({'error': 'Missing name parameter'})
               elif param == 1:
                  return jsonify({'error': 'Missing username parameter'})
               else:
                  return jsonify({'error': 'Missing age parameter'})
    
    user = User(name, age, username, 'Boita_User')
    return jsonify({"success": "User created"}), 201, {"Set-Cookie": f"session_id={user.serialize()}", "location": f"/api/user/me"}

@app.route('/api/update_user', methods=['POST'])
@require_session
def api_update_user():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    age = data.get('age')

    if not name or not username or not age:
        params = [name, username, age]
        
        for param in range(3):
            if params[param] == None:
               if param == 0:
                  return jsonify({'error': 'Missing name parameter'})
               elif param == 1:
                  return jsonify({'error': 'Missing username parameter'})
               else:
                  return jsonify({'error': 'Missing age parameter'})
               
    if get_user_session(request.cookies.get('session_id')) == username:
        user = User(name, age, username, 'Boita_User')
        print(data)
        update_user(data, user)
        print(vars(user))
        return jsonify({'success': 'User updated'})
    else:
       return jsonify({'error': 'Invalid User session'}),403

@app.route('/api/user/me', methods=['GET'])
@require_session
def api_user_me():
    informations = return_user_information(request.cookies.get('session_id'))
    
    if informations:
        return jsonify(informations)
    else:
        return jsonify({'error': 'Invalid User session'}), 403

@app.route('/api/check_url', methods=['POST'])
@require_session
def api_check_url():
   url = check_url(request.cookies.get('session_id'))
   data = request.get_json()

   if url:
      if data.get('method') == method[0]:
         response = requests.get(url)
         
         return jsonify({'Response': f'{response.text}'})
         
      elif data.get('method') == method[1]:
         response = requests.post(url, headers=data.get('headers'), json=data.get('data'))
         
         return jsonify({'Response': f'{response.text}'})
      else:
       return jsonify({'error': 'Invalid method'}), 403
   else:
      return jsonify({'error': 'url not found'}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
