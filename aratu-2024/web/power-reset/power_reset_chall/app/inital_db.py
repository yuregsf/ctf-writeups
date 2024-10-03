import uuid
import sqlite3
import os 
import random
import string
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

def random_string(length):
    letters = string.ascii_lowercase+string.ascii_uppercase+string.digits+string.punctuation
    return ''.join(random.choice(letters) for i in range(length))


def init_db():
    conn = sqlite3.connect('db/users.db')
    conn.execute('''
                CREATE TABLE users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                question1 TEXT,
                answer1 TEXT,
                question2 TEXT,
                answer2 TEXT,
                is_admin INTEGER DEFAULT 0 
                );
            ''')
    
    name = 'admin'
    username = 'admin'
    id = str(uuid.uuid4())
    email = 'admin@ugabunga.io'
    password = random_string(12)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    conn.execute('INSERT INTO users (id, username, name, password, email, is_admin) VALUES (?, ?, ?, ?, ?, 1)', 
                         (id, username, name, hashed_password, email))
    conn.commit()
    conn.close()



def check_db():
    print('Checking database')
    if os.path.exists('db/users.db'):
        print('Database exists')
        try:
            os.remove('db/users.db')
            print('Database removed')
        except Exception as e:
            print(f'Error removing database: {e}')
            return False
        init_db()
    else:
        init_db()


