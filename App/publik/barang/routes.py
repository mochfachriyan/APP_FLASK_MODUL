from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from flask import Flask, render_template , url_for, redirect, request, session

# ---- BARANG ---- #
status=[{'status' : 'Tersedia'},
        {'status' : 'Habis'}]

# TAMPILAN AWAL BARANG (KONSEP COMBINE TABLE)
@app.route('/barang',  methods=['GET'])
def barang():
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * 
                       FROM barang, suplier
                       where barang.id_suplier = suplier.id_suplier
                  ''')
    results = cursor.fetchall()

    #Mengambil data suplier
    cursor.execute('SELECT * FROM suplier WHERE id_suplier')
    suplier = cursor.fetchall()
    return render_template('publik/barang.html', container=results, suplier=suplier, status=status)
  
  
# TAMBAH BARANG
@app.route('/tambah-barang', methods=['GET', 'POST'])
def tambah_barang():
    if request.method == 'POST':
        # Create variables for easy access
        nama_barang = request.form['nama']
        id_suplier = request.form['id_suplier']
        harga = request.form['harga']
        status = request.form['status']
        # stok = request.form['stok']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO BARANG (nama_barang, id_suplier ,harga, status) VALUES (%s, %s, %s, %s)"
        value = (nama_barang, id_suplier, harga, status)
        cursor.execute(sql, value)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('barang'))
    else:
        # memakai modal di halaman yang sama dan belum memiliki notif
        return redirect(url_for('barang'))
      
#  EDIT BARANG
@app.route('/edit-barang', methods=['GET', 'POST'])
def edit_barang():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        id_barang = request.form['id_barang']
        nama = request.form['nama']
        harga = request.form['harga']
        id_suplier = request.form['id_suplier']
        status = request.form['status']
        sql = "UPDATE barang SET nama_barang=%s, harga=%s, id_suplier=%s, status=%s WHERE id_barang=%s"
        val = (nama, harga, id_suplier, status, id_barang)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('barang'))
    else:
        return redirect(url_for('barang'))
      
#  HAPUS BARANG
@app.route('/hapus-barang/<id_barang>', methods=['GET', 'POST'])
def hapus(id_barang):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM barang WHERE id_barang=%s', (id_barang,))
    mysql.connection.commit()
    return redirect(url_for('barang'))