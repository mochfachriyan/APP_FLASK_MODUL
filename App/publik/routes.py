from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from flask import Flask, render_template , url_for, redirect, request, session


# --- TAMPILAN HOME PUBLIK --- #
@app.route('/')    # route pertama kali dijalankan
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

    # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM USER WHERE USERNAME = %s AND PASSWORD = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['nama'] = account['nama']
            # session['nik'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            # return 'Logged in successfully!' DIGANTI DENGAN
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('publik/login.html', msg=msg)


# --- TAMPILAN HOME PROFILE --- #
@app.route('/register')
def register():
    return render_template('publik/register.html')
  
# HOME
@app.route('/dashboard')
def dashboard():
    # Mengecek jika user login masuk ke halaman home
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('publik/dashboard.html', nama=session['nama'])
    # jika tidak login masuk ke halaman login awal
    return redirect(url_for('login'))
  
# LOGOUT
@app.route('/logout')
def logout():
    # Remove session data, Untuk mengelurkan fungsi session / logout data
    session.pop('loggedin', None)
    session.pop('nama', None)
    session.pop('username', None)
    session.pop('nik', None)
    # Redirect to login page
    return redirect(url_for('login'))
  
# # REGISTER
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     msg = ''    # massange untuk jika dibutuhkan ditampilan awal
#     if request.method == 'POST':   # mengecek jika "username", "password" and "email" POST requests exist (user submitted form) # and 'id' in request.form and 'nama' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         nama = request.form['nama']
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM USER WHERE USERNAME = % s', (username, ))
#         account = cursor.fetchone()
#         if account:   #cek kalau akun sudah pernah dipakai
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  #untuk batasan email
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z]+', nama): #untuk batasan nama
#             msg = 'Invalid Name !'
#         elif not re.match(r'[A-Za-z0-9]+', username): #untuk batasan username
#             msg = 'Username must contain only characters and numbers !'
#         elif not username or not password or not nama:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO USER VALUES (%s, %s, %s, %s, %s )',
#                            (nama, username, password, email, ))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('login/register.html', msg=msg)
  
  