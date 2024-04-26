from flask import Flask, render_template, app, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('html.html')


@app.route('/redirect_to_login')
def redirect_to_login():
    return redirect(url_for('login'))
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/redirect_to_cart')
def redirect_to_cart():
    return redirect(url_for('cart'))
@app.route('/cart')
def cart():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0', port='5500')

