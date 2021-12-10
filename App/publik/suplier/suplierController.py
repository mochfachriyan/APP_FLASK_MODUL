from flask.helpers import url_for
from werkzeug.utils import redirect
from App import app, response, mysql
import MySQLdb.cursors
from flask import request, jsonify, send_file, Response

import pandas as pd
import io, csv
from io import BytesIO

import os 
from os.path import join, dirname, realpath

import xlrd


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
    
    
    
    
# -------------------------------------- IMPORT EXPORT EXCEL , CSV -------------------------------------------------------- #

# --- EXPORT EXCEL --- #
def suplierExportExcel():
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
  return send_file(output, attachment_filename="Suplier Excel.xlsx", as_attachment=True)



# --- EXPORT CSV --- #
def suplierExportCsv():
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
  return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=suplier CSV.csv"})


# --- IMPORT CSV --- #
def uploadFilesCsv():
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
    
    
# --- IMPORT EXCEL --- #
def uploadFilesExcel():
  # get the uploaded file
  uploaded_file = request.files['file']
  if uploaded_file.filename != '':
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    # set the file path
    uploaded_file.save(file_path)
    parseEXCEL(file_path)
    # save the file
  return redirect(url_for('suplier'))

def parseEXCEL(filePath):
  book = xlrd.open_workbook(filePath)
  # sheet = book.sheet_by_name('suplier')
  sheet = book.sheet_by_index(0)
  
  cursor = mysql.connection.cursor()
  query = 'INSERT INTO suplier (nama_suplier, no_telp, alamat) VALUES (%s, %s, %s)'
  
  for row in range(1, sheet.nrows):
        nama     = sheet.cell(row,0).value
        tlp      = sheet.cell(row,1).value
        alamat   = sheet.cell(row,2).value
        print(nama)
        values = (nama, tlp, alamat)
        cursor.execute(query, values)
        mysql.connection.commit()
        
  cursor.close()