from MySQLdb import connect
from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from App.publik.suplier import suplierController
from flask import Flask, render_template , url_for, redirect, send_file, request, session
import pandas as pd
from io import BytesIO

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


# ------------ EXPORT CSV ---------------- #
# @app.route('/suplier-export-csv')
# def suplier_export_csv():
#   try:
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute("SELECT id_suplier, nama_suplier, no_telp, alamat FROM suplier")
#     output = io.StringIO()
# 		writer = csv.writer(output)
    
    
#   except Exception as e:
#     print(e)



# ------------ IMPORT CSV ----------------#
@app.route('/suplier-import-csv')
def suplier_import_csv():
  return 'import'

  
# TODO kerjakan IMPORT CSV DULU
# TODO kerjakan JSON PEMBELIAN CRUD JSON
# TODO kerjakan IMPORT CSV DULU


