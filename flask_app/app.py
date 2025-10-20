# app.py - CRUD Pasien sederhana dengan Flask dan PyMySQL
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Konfigurasi database
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'db': 'rsud_sim',
    'cursorclass': pymysql.cursors.DictCursor
}

# Fungsi koneksi
def get_conn():
    return pymysql.connect(**DB_CONFIG)

# Halaman utama
@app.route('/')
def index():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM patients ORDER BY id ASC')
        patients = cur.fetchall()
    return render_template('patients.html', patients=patients)

# Tambah data pasien
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nama = request.form['nama']
        tgl_lahir = request.form['tgl_lahir']
        alamat = request.form['alamat']
        diagnosa = request.form['diagnosa']

        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO patients (nama, tgl_lahir, alamat, diagnosa) VALUES (%s, %s, %s, %s)',
                (nama, tgl_lahir, alamat, diagnosa)
            )
            conn.commit()
        return redirect(url_for('index'))

    return render_template('create_patient.html')

# Edit data pasien
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM patients WHERE id=%s', (id,))
        patient = cur.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']
        tgl_lahir = request.form['tgl_lahir']
        alamat = request.form['alamat']
        diagnosa = request.form['diagnosa']

        with conn.cursor() as cur:
            cur.execute(
                'UPDATE patients SET nama=%s, tgl_lahir=%s, alamat=%s, diagnosa=%s WHERE id=%s',
                (nama, tgl_lahir, alamat, diagnosa, id)
            )
            conn.commit()
        return redirect(url_for('index'))

    return render_template('edit_patient.html', patient=patient)

# Hapus data pasien
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM patients WHERE id=%s', (id,))
        # Reset urutan ID agar berurutan lagi
        cur.execute("SET @num := 0;")
        cur.execute("UPDATE patients SET id = @num := (@num + 1);")
        cur.execute("ALTER TABLE patients AUTO_INCREMENT = 1;")
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
