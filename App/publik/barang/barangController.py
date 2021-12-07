from logging import exception
from flask.helpers import url_for
from werkzeug.utils import redirect
from App import app, response, mysql
import MySQLdb.cursors
from flask import request, jsonify

from App.publik.suplier import suplierController

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
    
# -------------------------------------------------------------------   (BUAT EKSPERIMEN)
def cobaCoba(id_suplier):
  try:
    dataSuplier = suplierController.detailSuplier(id_suplier)
    
    if not dataSuplier:
      return response.badRequest([], 'Data Suplier tidak ada !!')
    
    return response.success(dataSuplier, "success")
  except Exception as e: 
    print(e)
# -------------------------------------------------------------------   (BUAT EKSPERIMEN)
    
# --- DETAIL BARANG BERDASARKAN ID AKAN MENAMPILKAN DETAIL SUPLIER --- #
def detailBarang(id_barang):   # Show all data suplier without condition
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    # SELECT QUERY DARI TABEL BARANG
    cursor.execute(''' SELECT id_barang,nama_barang,harga,id_suplier,status 
                       FROM barang 
                       where id_barang = %s''', (id_barang)) 
    dataBarang = cursor.fetchone()               # Fetch data dari query Select
    
    
    if not dataBarang:
      return response.badRequest([], 'Data karyawan tidak ada !!')
    
    dataSuplier = suplierController.detailSuplierBarang(id_barang)
    data = singleDetailSuplier(dataBarang, dataSuplier)
    
    
    return response.success(data, "success")
  except Exception as e: 
    print(e)
    
    
def singleDetailSuplier(barang, suplier):
  data = {
    'id_barang' : barang.get('id_barang'),
    'nama_barang': barang.get('nama_barang'),
    'harga' : barang.get('harga'),
    'status' : barang.get('status'),
    'suplier' : suplier                       #------- NESTED JSON, Data Suplier Semua akan di tampung disini
  }
  return data
    


# ===================================== POST (INSERT)
def tambahBarang():    
  try:
    nama_barang = request.form.get('nama_barang')
    harga = request.form.get('harga')
    id_suplier = request.form.get('id_suplier')
    status = request.form.get('status')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO BARANG (nama_barang, id_suplier ,harga, status) VALUES (%s, %s, %s, %s)"
    value = (nama_barang, id_suplier, harga, status)
    cursor.execute(sql, value)
    mysql.connection.commit() # Insert format tanggal menggunakan postman masih blm bisa
    cursor.close()
    return response.success('', 'Sukses menambahkan data Barang')
  except Exception as e:
    print(e)
    
    
# ===================================== PUT (UPDATE)
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
    val = (nama_barang, harga, id_suplier, status, id_barang)
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