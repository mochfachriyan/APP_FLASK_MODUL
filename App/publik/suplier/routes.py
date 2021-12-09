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

# ------------ EXPORT EXCEL ----------------#
@app.route('/suplier-export-excel')
def suplier_export_excel():
  cursor = mysql.connect
  df_1 = pd.read_sql_query('''  SELECT id_suplier, nama_suplier, no_telp, alamat 
                                FROM suplier 
                                ORDER BY id_suplier
                           ''', cursor)
  
   #create a random Pandas dataframe
    # df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))
  
  #create an output stream
  output = BytesIO()
  writer = pd.ExcelWriter(output, engine='xlsxwriter')
  
  #taken from the original question
  df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
  # df_1.to_excel(writer,startrow = len(df_1) + 4, merge_cells = False , sheet_name = "Sheet_1")                             

  workbook = writer.book
  worksheet = writer.sheets["Sheet_1"]
  format = workbook.add_format()
  format.set_bg_color('#3274d6')
  worksheet.set_column(1,9,28)
  
  #the writer has done its job
  writer.close()

  #go back to the beginning of the stream
  output.seek(0)

  #finally return the file
  return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)


# ------------ EXPORT CSV ----------------#
@app.route('/suplier-export-csv')
def suplier_export_csv():
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute("SELECT id_suplier, nama_suplier, no_telp, alamat FROM suplier")
  result = cursor.fetchall()

  output = io.StringIO()
  writer = csv.writer(output)
  
  line = ['id suplier, nama suplier, no_telp, alamat']
  writer.writerow(line)

  for row in result:
    line = [str(row['id_suplier']) + ',' + row['nama_suplier'] + ',' + row['no_telp'] + ',' + row['alamat']]
    writer.writerow(line)

  output.seek(0)
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=suplier.csv"})








# ------------ IMPORT CSV ----------------#
# Menuju Ke Upload Suplier
@app.route('/suplier-upload')
def uploadSuplier():
  return render_template('publik/upload.html')

# Upload folder  -----> Belum dipindah ke route / run.py agar file rapih 
UPLOAD_FOLDER = 'App/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER    
    
# Get the uploaded files
@app.route('/suplier-upload-csv', methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
      return redirect(url_for('suplier'))
    
def parseCSV(filePath):
      # CVS Column Names
      col_names = ['nama_suplier','no_telp','alamat']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvData.iterrows():
             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
             sql = "INSERT INTO suplier (nama_suplier, no_telp, alamat) VALUES (%s, %s, %s)"
             value = (row['nama_suplier'],row['no_telp'],row['alamat'])
             cursor.execute(sql, value)
             mysql.connection.commit()
             print(i,row['nama_suplier'],row['no_telp'],row['alamat'])
    


  
  
  
  
  
# TODO kerjakan EXPORT CSV DULU (
# TODO kerjakan JSON PEMBELIAN CRUD JSON
# DONE kerjakan IMPORT CSV DULU


