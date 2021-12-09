from App import app   # --- Menjalankan app dari file App/_init_.py yang sudah di deklarasi --- #

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Detail Dari koneksi database yang akan di hubungkan menggunakan mysql (xampp)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_belajarflask'

# Untuk konfigurasi upload file dan directorie file
UPLOAD_FOLDER = 'App/static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER   

if __name__ == '__main__':
    app.run(debug=True)
