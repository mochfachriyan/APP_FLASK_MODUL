from logging import exception
from flask.helpers import url_for
from werkzeug.utils import redirect
from App import app, response, mysql
import MySQLdb.cursors
from flask import request, jsonify, send_file, Response

from App.publik.suplier import suplierController

import pandas as pd
import io, csv
from io import BytesIO

import os 
from os.path import join, dirname, realpath

import xlrd


# ===================================== GET ALL DATA (READ)
def tabelBarang():   # Show all data suplier without condition
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    cursor.execute('SELECT id_barang,nama_barang,harga,id_suplier,status FROM barang') 
    data = cursor.fetchall()               # Fetch data dari query Select
    cursor.close()
    # return jsonify(data) # Menampilkan data dengan json
    return response.success(data, "success")
  except Exception as e: 
    print(e)
    
# --- DETAIL BARANG BERDASARKAN ID AKAN MENAMPILKAN DETAIL SUPLIER --- #
def detailBarang(id_barang):   # Show all data barang
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    # SELECT QUERY DARI TABEL BARANG
    cursor.execute(''' SELECT id_barang,nama_barang,harga,id_suplier,status 
                       FROM barang 
                       where id_barang = %s
                  ''', (id_barang,)) 
    dataBarang = cursor.fetchone()               # Fetch data dari query Select
    
    
    
    if not dataBarang:
      return response.badRequest([], 'Data karyawan tidak ada !!')
    
    dataSuplier = suplierController.detailSuplierBarang(id_barang)
    dataJson = singleDetailSuplier(dataBarang, dataSuplier)
    
    
    return response.success(dataJson, "success")
  except Exception as e: 
    print(e)
    
    
def singleDetailSuplier(barang, v_suplier):
  dataJson = {
    'id_barang' : barang.get('id_barang'),
    'nama_barang': barang.get('nama_barang'),
    'harga' : barang.get('harga'),
    'status' : barang.get('status'),
    # 'id_suplier' : barang.get('id_suplier'),
    'suplier': v_suplier,                     #------- NESTED JSON, Data Suplier Semua akan di tampung disini
  }
  return dataJson
    


# --------------------------------------- POST (INSERT)
def tambahBarang():    
  try:
    nama_barang = request.form.get('nama_barang')
    harga = request.form.get('harga')
    id_suplier = request.form.get('id_suplier')
    status = request.form.get('status')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO BARANG (nama_barang, harga, id_suplier, status) VALUES (%s, %s, %s, %s)"
    value = (nama_barang, harga, id_suplier, status,)
    cursor.execute(sql, value)
    mysql.connection.commit() # Insert format tanggal menggunakan postman masih blm bisa
    cursor.close()
    return response.success('', 'Sukses menambahkan data Barang')
  except Exception as e:
    print(e)
    
    
# ------------------------------------ PUT (UPDATE)
def editBarang(id_barang):   
  try:
    nama_barang = request.form.get('nama_barang') # get value dari postman saat PUT berlangsung
    harga = request.form.get('harga')
    id_suplier = request.form.get('id_suplier')
    status = request.form.get('status')
    
    input = [                             # --- INPUTAN VALUE UNTUK DI UBAH 
      {
        'nama_barang' : nama_barang,        
        'harga' : harga,
        'id_suplier' : id_suplier,
        'status' : status
      }
    ]
    
    dataBarang = detailBarang(id)   # ---- AMBIL DATA DETAIL BARANG UNTUK MENGETAHUI BARANG YG DI EDIT ADA ATAU TIDAK ADA
    
    if not dataBarang:
      return response.badRequest([], 'Data Barang Tidak Ada !!!')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "UPDATE barang SET nama_barang=%s, harga=%s, id_suplier=%s, status=%s WHERE id_barang=%s"
    val = (nama_barang, harga, id_suplier, status, id_barang,)
    cursor.execute(sql, val)
    mysql.connection.commit()
    cursor.close()
    return response.success(input, 'Succees Update Data Barang !!') # Menampilkan data yang di update melalui postman. Kalau ga di update value nya null
  except Exception as e:
    print(e)
    
    
# ===================================== PUT (Delete)
def deleteBarang(id_barang):
  try:
    dataBarang = detailBarang(id_barang)
    
    if dataBarang is None:   # Cek datanya ada atau tidak
      return response.badRequest([], "id Barang  tidak ada !!!")
    else:
      cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cursor.execute('DELETE FROM barang WHERE id_barang=%s', (id_barang,))
      mysql.connection.commit()
      cursor.close()
      return response.success(id_barang, "Data berhasil dihapus !!!")
  except Exception as e:
    print(e)
    
    
    
# -------------------------------------- IMPORT EXPORT EXCEL , CSV -------------------------------------------------------- #
  
# --- EXPORT EXCEL --- #
def barangExportExcel():
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



# --- EXPORT CSV --- #
def BarangExportCsv():
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
