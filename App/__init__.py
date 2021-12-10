from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__) # --- app(variabel) yang sudah di deklarasi yang digunkan di route dan akan dijalankan di run.py --- #

# Intialize MySQL
mysql = MySQL(app)

from App.publik import routes # --- import dari setiap route folder yang nantinya akan di jalankan ke run.py --- #
from App.admin import routes
from App.publik.barang import routes
from App.templates.publik.upload import routes
from App.publik.pembelian import routes



