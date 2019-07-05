from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'logindb'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/logindb'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        #print session['username']
        return render_template('logout.html')
        #session.clear()
        #return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.usertable
    login_user = users.find_one({'name' : request.form['username']})
    print(login_user)
    if login_user:
        if  request.form['pass']== login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()

    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.usertable
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:

            users.insert({'name' : request.form['username'], 'password' :  request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
