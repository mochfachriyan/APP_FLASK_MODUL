from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from flask import Flask, render_template , url_for, redirect, request, session

#  -------- PEMBELIAN ----------- #
@app.route('/pembelian', methods=['GET', 'POST'])
def pembelian():
    cursor = mysql.connection.cursor()
    cursor.execute('''  SELECT * 
                        FROM xxx_pembelian, barang, user, suplier
                        WHERE xxx_pembelian.id_barang = barang.id_barang
                        AND xxx_pembelian.id_user = user.id_user
                        AND barang.id_suplier = suplier.id_suplier
                        ORDER BY xxx_pembelian.id_barang
                   ''')
    results = cursor.fetchall()

    # Mengambil Data dari tabel BARANG
    cursor.execute('SELECT * FROM barang')
    barang = cursor.fetchall()

    # Mengambil Data dari tabel SUPLIER
    cursor.execute('SELECT * FROM suplier')
    suplier = cursor.fetchall()

    # Mengambil Data dari tabel USER
    cursor.execute('SELECT * FROM user')
    user = cursor.fetchall()
    
    return render_template('publik/pembelian.html', container=results, barang=barang, suplier=suplier, user=user)
  
#   TAMBAH PEMBELIAN
@app.route('/tambah-pembelian', methods=['GET', 'POST'])
def tambah_pembelian():
    if request.method == 'POST':
        # Create variables for easy access
        user = request.form['id_user']
        barang = request.form['id_barang']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO xxx_pembelian ( id_user, id_barang ) VALUES (%s,%s)"
        value = (user, barang,)
        cursor.execute(sql, value)
        mysql.connection.commit()
        return redirect(url_for('pembelian'))
    else:
        # memakai modal di halaman yang sama
        return redirect(url_for('pembelian'))
      
#  EDIT PEMBELIAN
@app.route('/edit-pembelian', methods=['GET', 'POST'])
def edit_pembelian():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        pembelian = request.form['id_pembelian']
        user = request.form['id_user']
        barang = request.form['id_barang']
        sql = "UPDATE xxx_pembelian SET id_user=%s, id_barang=%s WHERE id_pembelian=%s"
        val = (user, barang, pembelian)
        cursor.execute(sql, val)
        mysql.connection.commit()
        return redirect(url_for('pembelian'))
    else:
        return redirect(url_for('pembelian'))
      
      
#  HAPUS PEMBELIAN
@app.route('/hapus-pembelian/<id_pembelian>', methods=['GET', 'POST'])
def hapus_pembelian(id_pembelian):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM xxx_pembelian WHERE id_pembelian=%s', (id_pembelian,))
    mysql.connection.commit()
    return redirect(url_for('pembelian'))