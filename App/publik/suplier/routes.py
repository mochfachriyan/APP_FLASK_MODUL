from MySQLdb import connect
from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from App.publik.suplier import suplierController
from flask import Flask, render_template , url_for, redirect, send_file, request, session, Response
import pandas as pd
import io, csv
from io import BytesIO

import os 
from os.path import join, dirname, realpath

# ---- SUPLIER ---- #

#  HOME SUPLIER
@app.route('/suplier', methods=['GET'])
def suplier():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM SUPLIER')
    results = cursor.fetchall()
    return render_template('publik/suplier.html', container=results )
  
#   TAMBAH SUPPLIER
@app.route('/tambah-suplier', methods=['GET', 'POST'])
def tambah_suplier():
    if request.method == 'POST':
        # Create variables for easy access
        nama = request.form['nama']
        no_tlp = request.form['no_tlp']
        alamat = request.form['alamat']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO SUPLIER (nama_suplier, no_telp, alamat) VALUES (%s,%s,%s)"
        value = (nama, no_tlp, alamat)
        cursor.execute(sql, value)
        mysql.connection.commit()
        return redirect(url_for('suplier'))
    else:
        # memakai modal di halaman yang sama
        return redirect(url_for('suplier'))
  
#   EDIT SUPLIER
@app.route('/edit-suplier', methods=['GET', 'POST'])
def edit_suplier():
    cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM barang WHERE id_barang=%s', ( id_barang, )) #ini kenapa harus pakai koma
    # data = cursor.fetchone()
    if request.method == 'POST':
        id_suplier = request.form['id_suplier']
        nama = request.form['nama']
        no_tlp = request.form['no_tlp']
        alamat = request.form['alamat']
        sql = "UPDATE SUPLIER   SET nama_suplier=%s, no_telp=%s, alamat=%s WHERE id_suplier=%s"
        val = (nama, no_tlp, alamat, id_suplier)
        cursor.execute(sql, val)
        mysql.connection.commit()
        return redirect(url_for('suplier'))
    else:
        return redirect(url_for('suplier'))

#  HAPUS SUPLIER
@app.route('/hapus-suplier/<id_suplier>', methods=['GET', 'POST'])
def hapus_suplier(id_suplier):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM SUPLIER WHERE id_suplier=%s', (id_suplier,))
    mysql.connection.commit()
    return redirect(url_for('suplier'))
  
  
# --- KODINGAN UNTUK ROUTE UNTUK MENAMPILKAN JSON --- #

# --- HOME SUPLIER --- # 
@app.route('/suplier-json', methods=['GET','POST'])   # [GET] untuk menampilkan data 
def suplierJson():   
  if request.method == 'POST':
    return suplierController.tambahSuplier() # --- TAMBAH SUPLIER --- #
  else:
    return suplierController.tabelSuplier() # --- TABEL SUPLIER --- #

# --- DETAIL SUPLIER --- # 
@app.route('/suplier-json/<id_suplier>', methods=['GET'])
def suplierJsonDetails  (id_suplier):
  return suplierController.detailSupliers(id_suplier) # --- DETAIL SUPLIER --- #
  
  
  
# --- TES --- # 
@app.route('/tes/<id_barang>', methods=['GET'])
def tes(id_barang):
  return suplierController.detailSuplierBarang(id_barang) # --- DETAIL SUPLIER --- #



# --- KODINGAN UNTUK ROUTE UNTUK EXPORT DAN IMPORT EXCEL --- #

# ------------ EXPORT EXCEL -------------- #
@app.route('/suplier-export-excel')
def suplier_export_excel():
  return suplierController.suplierExportExcel()


# ------------ EXPORT CSV ---------------- #
@app.route('/suplier-export-csv')
def suplier_export_csv():
  return suplierController.suplierExportCsv()


# ------------ IMPORT CSV ---------------- #
# Menuju Ke Upload Suplier
@app.route('/suplier-upload-csv')
def upload_suplier():
  return render_template('publik/upload.html')

# ------------ IMPORT CSV ---------------- #
@app.route('/suplier-save-csv', methods=['POST'])
def save_files_csv():
  return suplierController.uploadFilesCsv()
    


  
  
  
  
  
# DONE kerjakan EXPORT CSV DULU (
# TODO kerjakan JSON PEMBELIAN CRUD JSON
# DONE kerjakan IMPORT CSV DULU


