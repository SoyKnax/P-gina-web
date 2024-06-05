from flask import Flask, app, render_template, redirect, url_for, flash, request 
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '1106'  # Necesario para usar flash

db_config = {
    'user': 'Admin',
    'password': 'Admin',
    'host': 'localhost',
    'database': 'users'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect_to_register')
def redirect_to_register():
    return redirect(url_for('register'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        names = request.form['names']
        emails = request.form['emails']
        passwords = request.form['passwords']
        
        hashed_password = generate_password_hash(passwords)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO about (names, emails, passwords) VALUES (%s, %s, %s)", (names, emails, hashed_password))
            conn.commit()
            flash('Usuario registrado con éxito')
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        emails = request.form['emails']
        passwords = request.form['passwords']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM about WHERE emails = %s", (emails,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[3], passwords):
            flash('Inicio de sesión exitoso')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas')
    
    return render_template('login.html') 

@app.route('/reg_users')
def reg_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT names, emails FROM about")
    about = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reg_users.html', about=about)
    
@app.route('/cart')
def cart():
    return render_template('cart.html')
@app.route('/redirect_to_cart')
def redirect_to_cart():
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0', port='5500')

