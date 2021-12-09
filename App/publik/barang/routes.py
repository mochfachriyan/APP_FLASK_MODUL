from App import app   # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi --- #
from App import mysql
import MySQLdb.cursors
import re
from App.publik.barang import barangController
from flask import Flask, render_template , url_for, redirect, request, session, send_file, Response
import pandas as pd
import io, csv
from io import BytesIO

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
  
  
  
# --- KODINGAN UNTUK ROUTE UNTUK MENAMPILKAN JSON --- #

# --- HOME BARANG --- # 
@app.route('/barang-json', methods=['GET','POST'])   # [GET] untuk menampilkan data 
def barangJson():   
  if request.method == 'POST':
    return barangController.tambahBarang()  # --- TAMBAH BARANG --- #
  else:
    return barangController.tabelBarang() # --- SEMUA BARANG --- #
  
# --- BARANG --- # 
@app.route('/barang-json/<id_barang>', methods=['GET','PUT','DELETE'])
def barangJsonDetail(id_barang):
  if request.method == 'GET':
    return barangController.detailBarang(id_barang) # --- DETAIL BARANG --- #
  elif request.method == 'PUT':
    return barangController.editBarang(id_barang) # --- EDIT BARANG --- #
  else:
    return barangController.deleteBarang(id_barang) # --- HAPUS BARANG --- #


# --- KODINGAN UNTUK ROUTE UNTUK EXPORT DAN IMPORT EXCEL --- #

# ------------ EXPORT EXCEL ----------------#
@app.route('/barang-export-excel')
def barang_export_excel():
  cursor = mysql.connect
  df_1 = pd.read_sql_query('''  SELECT id_barang, nama_barang, harga, id_suplier, status 
                                FROM barang 
                                ORDER BY id_barang
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
  return send_file(output, attachment_filename="testing_barang.xlsx", as_attachment=True)


# ------------ EXPORT CSV ----------------#
@app.route('/barang-export-csv')
def barang_export_csv():
  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cursor.execute('''  SELECT id_barang, nama_barang, harga, id_suplier, status 
                      FROM barang 
                      ORDER BY id_barang''')
  result = cursor.fetchall()

  output = io.StringIO()
  writer = csv.writer(output)
  
  line = ['id barang, nama barang, harga, id_suplier, status']
  writer.writerow(line)

  for row in result:
    line = [str(row['id_barang']) + ',' + row['nama_barang'] + ',' + str(row['harga']) + ',' + str(row['id_suplier']) + ',' + row['status']]
    writer.writerow(line)

  output.seek(0)
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=barang.csv"})
