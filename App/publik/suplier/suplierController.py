from flask.helpers import url_for
from werkzeug.utils import redirect
from App import app, response, mysql
import MySQLdb.cursors
from flask import request, jsonify


# ===================================== GET ALL DATA (READ)
def tabelSuplier():   # Show all data suplier without condition
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    cursor.execute('SELECT id_suplier,nama_suplier,no_telp,alamat FROM suplier ORDER BY id_suplier') 
    data = cursor.fetchall()               # Fetch data dari query Select
    cursor.close()
    # return jsonify(data) # Menampilkan data dengan json
    return response.success(data, "success")
  except Exception as e: 
    print(e)
    
def detailSupliers(id_suplier):
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    cursor.execute(''' SELECT id_suplier,nama_suplier,no_telp,alamat 
                       FROM suplier 
                       where id_suplier = %s
                  ''', (id_suplier,)) 
    suplier = cursor.fetchone()               # Fetch data dari query Select
    cursor.close()
    
    if not suplier:
      return response.badRequest([], 'Data Suplier tidak ada !!')
    
    return  response.success(suplier, "success")
  except Exception as e:
    print(e)
    
#-----TIDAK PERLU FORMAT ARRAY KARENA FETCHALL SUDAH DALAM BENTUK ARRAY DAN SINGEL OBJECT-----#
# def formatArray(datas):
#     array = []  
#     for i in datas:
#       array.append(singleObjectSuplier(i)) # INGAT pelajaran di w3school tentang Lists, Tuples, Sets, DIctionaries ? nah ini method yang ada di Lists
#                       # menambahkan di arraynya
#                       # membuat Function singleObject dulu
#     return array

# def singleObjectSuplier(dataSuplier):
#   dataSuplier={
#     'id_suplier': dataSuplier.id_suplier,
#     'nama_suplier': dataSuplier.nama_suplier,
#     'no_telp': dataSuplier.no_telp,
#     'alamat': dataSuplier.alamat      #  bisa menampilkan kolom lain - tergantung query 
#   }
#   return dataSuplier

# --- DETAIL SUPLIER UNTUK DITAMPILKAN DI DETAIL BARANG BERDASARAKAN ID BARANG --- #
def detailSuplierBarang(id_barang):  # ---- khusus untuk tampilan detail suplier berdasarkan ID Barang
  try:
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
    cursor.execute(''' SELECT suplier.id_suplier, suplier.nama_suplier, suplier.no_telp, suplier.alamat
                       FROM barang, suplier
                       where barang.id_suplier = suplier.id_suplier
                       and id_barang = %s
                   ''', (id_barang,)) 
    suplierBarang = cursor.fetchone()               # Fetch data dari query Select
    cursor.close()
    
    return suplierBarang
    
  except Exception as e:
    print(e)
  
  # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)     # akses ke database
  # cursor.execute(''' SELECT id_suplier, nama_suplier, no_telp, alamat 
  #                   FROM suplier 
  #                   where id_suplier = %s
  #               ''', (id_suplier)) 
  # suplier = cursor.fetchone()               # Fetch data dari query Select
  # cursor.close()
  


# ===================================== POST (INSERT)
def tambahSuplier():    
  try:
    nama_suplier = request.form.get('nama_suplier')
    no_tlp = request.form.get('no_telp')
    alamat = request.form.get('alamat')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO suplier (nama_suplier, no_telp, alamat) VALUES (%s,%s,%s)"
    value = (nama_suplier, no_tlp, alamat,)
    cursor.execute(sql, value)
    mysql.connection.commit() # Insert format tanggal menggunakan postman masih blm bisa
    cursor.close()
    # returnnya
    return response.success('', 'Sukses menambahkan data Suplier')
  except Exception as e:
    print(e)






  
 
  