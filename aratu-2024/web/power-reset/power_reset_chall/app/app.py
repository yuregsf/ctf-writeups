from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
import uuid
import hashlib
from functools import wraps
from flask_bcrypt import Bcrypt
import inital_db

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = inital_db.random_string(32)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def verify_question(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user['question1'] == None or g.user['question2'] == None:
            flash('Please set security questions', 'error')
            return redirect(url_for('set_security_questions'))
        return f(*args, **kwargs)
    return decorated_function


def verify_set_password(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'set_password' not in session:
            flash('Please verify security questions', 'error')
            return redirect(url_for('forgot_password_questions'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    conn = sqlite3.connect('db/users.db', timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def before_request():
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        g.user = user
    else:
        g.user = None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        try:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        except sqlite3.Error as e:
            print(e)
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (id, username, name, password, email) VALUES (?, ?, ?, ?, ?)', 
                         (user_id, username, name, hashed_password, email))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.close()
            flash(f'Username or email already exists: {e}', 'error')
            return render_template('register.html')
        except sqlite3.Error as e:
            conn.close()
            flash(f'An error occurred: {e}', 'error')
            return render_template('register.html')

        conn.close()
        session['user_id'] = user_id
        return redirect(url_for('set_security_questions'))
    return render_template('register.html')


@app.route('/set_security_questions', methods=['GET', 'POST'])
@login_required
def set_security_questions():
    if request.method == 'POST':
        question1 = request.form['question1']
        answer1 = request.form['answer1']
        question2 = request.form['question2']
        answer2 = request.form['answer2']
        user_id = session['user_id']

        conn = get_db_connection()
        conn.execute('UPDATE users SET question1 = ?, answer1 = ?, question2 = ?, answer2 = ? WHERE id = ?', 
                     (question1, answer1, question2, answer2, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('profile'))
    
    return render_template('set_security_questions.html')

@app.route('/profile')
@login_required
@verify_question
def profile():
    flag = None
    conn = get_db_connection()
    type_user_row = conn.execute('SELECT is_admin FROM users WHERE id = ?', 
                                (session['user_id'],)).fetchone()
    conn.close()
    type_user = type_user_row['is_admin'] if type_user_row else None

    if type_user == 1:  
        print('You are admin')
        with open('/flag.txt', 'r') as file:
            flag = file.read().strip()

    return render_template('profile.html', flag=flag)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        conn = get_db_connection()
        user = conn.execute('SELECT id FROM users WHERE username = ? AND email = ?', (username, email)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('forgot_password_questions'))
        else:
            flash('Invalid username or email', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')


@app.route('/forgot_password_questions', methods=['GET', 'POST'])
@login_required
@verify_question
def forgot_password_questions():
    conn = get_db_connection()
    user = conn.execute('SELECT question1, question2 FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()

    if request.method == 'POST':
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']

        if user:
            conn = get_db_connection()
            user_valid = conn.execute('SELECT * FROM users WHERE id = ? AND answer1 = ? AND answer2 = ?',
                                    (session['user_id'], answer1, answer2)).fetchone()
            conn.close()

            if user_valid:
                session['set_password'] = True
                return redirect(url_for('reset_password'))
            else:
                flash('Invalid answers', 'error')
                return redirect(url_for('forgot_password'))
        
    return render_template('forgot_password_questions.html', question1=user['question1'], question2=user['question2'])


@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
@verify_set_password
def reset_password():
    uuid_user = session['user_id']
    if request.method == 'POST':
        password = request.form['password'].encode('utf-8')
        repeat_password = request.form['confirm_password'].encode('utf-8')
        user_id = request.form['id']

        if password != repeat_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('reset_password'))
        
        new_hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        conn.execute('UPDATE users SET password = ? WHERE id = ?',
                    (new_hashed_password, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('profile'))
    return render_template('reset_password.html', id=uuid_user)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    inital_db.check_db()
    app.run(host='0.0.0.0')