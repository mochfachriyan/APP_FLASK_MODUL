from App import app  # --- import app(variable) dari file App/_init_.py yang sudah di deklarasi yang akan di gunakan di route --- #
from flask import Flask, render_template

# --- TAMPILAN HOME ADMIN --- #
@app.route('/admin/home')
def home_admin():
    return render_template('admin/index.html')

# --- TAMPILAN HOME ADMIN --- #
@app.route('/admin/profile')
def profile_admin():
    return 'About Admin!!!'