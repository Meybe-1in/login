from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Conexión a la base de datos MongoDB
client = MongoClient('mongodb+srv://meybe:pitufo.15@user.vdiqemk.mongodb.net/?retryWrites=true&w=majority')
db = client['test_db']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('index.html')

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')


#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return render_template('register.html', error='Email already exists')
        else:
            password = generate_password_hash(request.form['password'])
            users_collection.insert_one({'email': email, 'password': password})
            return redirect(url_for('login'))
    return render_template('register.html')
#profile pagina logeada
@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        return render_template('profile.html', email=email)
    return redirect(url_for('login'))

#cerrar sesion
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
